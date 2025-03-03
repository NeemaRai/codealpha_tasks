import nltk
import json
import random
import numpy as np
import tensorflow as tf
import os
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import SGD
from nltk.stem import WordNetLemmatizer

# Download NLTK resources if not available
#nltk.download('punkt')
#nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Load intents JSON file
if not os.path.exists('intents.json'):
    raise FileNotFoundError("Error: 'intents.json' not found!")

with open('intents.json', encoding='utf-8') as file:
    intents = json.load(file)

# Data preprocessing
words = []
classes = []
documents = []
ignore_words = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatization and sorting
words = sorted(set(lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words))
classes = sorted(set(classes))

# Training data preparation
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = [lemmatizer.lemmatize(w.lower()) for w in doc[0]]
    for w in words:
        bag.append(1 if w in pattern_words else 0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)

# Ensure training data is valid
if len(training) == 0:
    raise ValueError("Error: Training data is empty! Check your preprocessing steps.")

train_x = np.array([i[0] for i in training], dtype=np.float32)
train_y = np.array([i[1] for i in training], dtype=np.float32)

# Save processed data
with open("training_data.pkl", "wb") as f:
    pickle.dump({"words": words, "classes": classes, "train_x": train_x, "train_y": train_y}, f)

# Build model
model = Sequential([
    Input(shape=(len(train_x[0]),)),  # Corrected input layer
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(len(train_y[0]), activation='softmax')
])

# Compile model
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train model
#model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=0)  # No output at all


# Save model in recommended format
model.save("chatbot_model.keras")  # Fixed warning for saving in HDF5 format

# Load trained model
def load_model():
    if not os.path.exists("chatbot_model.keras") or not os.path.exists("training_data.pkl"):
        raise FileNotFoundError("Error: Trained model or data file not found. Train the model first.")

    global model
    model = tf.keras.models.load_model("chatbot_model.keras")
    with open("training_data.pkl", "rb") as f:
        data = pickle.load(f)
    return data

# Load data and model
data = load_model()
words, classes = data["words"], data["classes"]

def clean_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

def bow(sentence, words):
    sentence_words = clean_sentence(sentence)
    bag = [1 if w in sentence_words else 0 for w in words]
    return np.array(bag)

def classify(sentence):
    ERROR_THRESHOLD = 0.30
    bow_data = bow(sentence, words).reshape(1, -1)
    results = model.predict(bow_data, verbose=0)[0]  # Suppressed verbose warning
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    return [(classes[r[0]], r[1]) for r in results] if results else [("unknown", 0)]

def response(sentence):
    results = classify(sentence)
    if results[0][0] == "unknown":
        return "I'm sorry, I don't understand. Can you rephrase your question?"
    
    for intent in intents['intents']:
        if intent['tag'] == results[0][0]:
            return random.choice(intent['responses'])
    
    return "I'm sorry, I don't understand."

# **Interactive chatbot loop**
def chatbot():
    print("Hello! I am an FAQ chatbot. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            print("Chatbot: Please enter a valid question.")
            continue

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! Have a great day! 😊")
            break

        response_text = response(user_input)
        print(f"Chatbot: {response_text}")

# Run chatbot
if __name__ == "__main__":
    chatbot()
