from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator

# Language Code Dictionary (Google Translate supports these codes)
LANGUAGES = {
    'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'assamese': 'as',
    'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn',
    'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny',
    'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr',
    'czech': 'cs', 'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en',
    'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr',
    'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn',
    'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi',
    'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id',
    'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk',
    'khmer': 'km', 'kinyarwanda': 'rw', 'konkani': 'gom', 'korean': 'ko', 'krio': 'kri', 'kurdish (kurmanji)': 'ku',
    'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lingala': 'ln',
    'lithuanian': 'lt', 'luganda': 'lg', 'luxembourgish': 'lb', 'macedonian': 'mk', 'maithili': 'mai',
    'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr',
    'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my', 'nepali': 'ne',
    'norwegian': 'no', 'odia (oriya)': 'or', 'oromo': 'om', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl',
    'portuguese': 'pt', 'punjabi': 'pa', 'quechua': 'qu', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm',
    'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn',
    'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es',
    'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt',
    'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts', 'turkish': 'tr', 'turkmen': 'tk',
    'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi',
    'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
}

root = tk.Tk()
root.title('Language Translator')
root.geometry('600x400')

frame1 = Frame(root, width=600, height=400, relief=RIDGE, borderwidth=5, bg='#F7DC6F')
frame1.place(x=0, y=0)

Label(root, text='Language Translator', font=('Helvetica', 20, 'bold'), fg='black', bg='#F7DC6F').pack(pady=10)
def translate():
    source_text = text_entry1.get('1.0', 'end-1c').strip()
    src_lang = auto_select.get()
    tgt_lang = choose_language.get()

    if not source_text:
        messagebox.showerror('Error', 'Enter text to translate!')
        return

    if src_lang not in LANGUAGES or tgt_lang not in LANGUAGES:
        messagebox.showerror('Error', 'Select valid languages!')
        return

    try:
        translated_text = GoogleTranslator(source=LANGUAGES[src_lang], target=LANGUAGES[tgt_lang]).translate(source_text)
        text_entry2.delete('1.0', 'end')
        text_entry2.insert('end', translated_text)
    except Exception as e:
        messagebox.showerror('Translation Error', str(e))

def clear():
    text_entry1.delete('1.0', 'end')
    text_entry2.delete('1.0', 'end')

# Language Selection Dropdowns
a = tk.StringVar()
auto_select = ttk.Combobox(frame1, width=27, textvariable=a, state='readonly', font=('verdana', 10, 'bold'))
auto_select['values'] = list(LANGUAGES.keys())
auto_select.place(x=15, y=60)
auto_select.current(0)

l = tk.StringVar()
choose_language = ttk.Combobox(frame1, width=27, textvariable=l, state='readonly', font=('verdana', 10, 'bold'))
choose_language['values'] = list(LANGUAGES.keys())
choose_language.place(x=305, y=60)
choose_language.current(1)

# Text Input and Output Boxes
text_entry1 = Text(frame1, width=25, height=7, borderwidth=5, relief=RIDGE, font=('verdana', 12))
text_entry1.place(x=10, y=100)
text_entry2 = Text(frame1, width=25, height=7, borderwidth=5, relief=RIDGE, font=('verdana', 12))
text_entry2.place(x=310, y=100)

# Buttons
btn1 = Button(frame1, command=translate, text='Translate', relief=RAISED, borderwidth=2,font=('verdana', 10, 'bold'), bg='#248aa2', fg='white', cursor='hand2')
btn1.place(x=190, y=300)

btn2 = Button(frame1, command=clear, text='Clear', relief=RAISED, borderwidth=2,font=('verdana', 10, 'bold'), bg='#248aa2', fg='white', cursor='hand2')
btn2.place(x=300, y=300)

root.mainloop()
