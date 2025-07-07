from tkinter import *
from tkinter import ttk
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import playsound
import os

translator = Translator()
dark_mode = False


LIGHT_BG = "#E3F2FD"
LIGHT_TEXT = "#0D47A1"
LIGHT_TEXTBOX = "#FFFFFF"
DARK_BG = "#0D1B2A"
DARK_TEXT = "#BBDEFB"
DARK_TEXTBOX = "#1B263B"
ACCENT = "#4285F4"


LANGUAGES = {
    'Auto': 'auto',
    'English': 'en',
    'Hindi': 'hi',
    'Gujarati': 'gu',
    'Marathi': 'mr',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese': 'zh-cn',
    'Japanese': 'ja',
    'Arabic': 'ar',
}



def translate_text():
    input_text = input_box.get("1.0", "end-1c")
    src_lang = LANGUAGES.get(source_lang.get(), 'auto')
    tgt_lang = LANGUAGES.get(target_lang.get(), 'hi')
    try:
        translated = translator.translate(input_text, src=src_lang, dest=tgt_lang)
        translated_text = translated.text
        output_box.config(state=NORMAL)
        output_box.delete("1.0", END)
        output_box.insert(END, translated_text)
        output_box.config(state=DISABLED)
    except Exception as e:
        output_box.config(state=NORMAL)
        output_box.delete("1.0", END)
        output_box.insert(END, f"Error: {e}")
        output_box.config(state=DISABLED)

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        bg, fg, box_bg = DARK_BG, DARK_TEXT, DARK_TEXTBOX
        toggle_btn.config(text="Switch to Light Mode")
    else:
        bg, fg, box_bg = LIGHT_BG, LIGHT_TEXT, LIGHT_TEXTBOX
        toggle_btn.config(text="Switch to Dark Mode")
    root.config(bg=bg)
    for widget in widgets:
        if isinstance(widget, Text):
            widget.config(bg=box_bg, fg=fg, insertbackground=fg)
        else:
            widget.config(bg=bg, fg=fg)
    title_label.config(fg=ACCENT)
    translate_btn.config(bg=ACCENT, fg="blue")
    toggle_btn.config(bg=ACCENT, fg="blue")
    clear_btn.config(bg=ACCENT, fg="blue")
    copy_btn.config(bg=ACCENT, fg="blue")
    record_btn.config(bg=ACCENT, fg="blue")
    speak_btn.config(bg=ACCENT, fg="blue")

def clear_text():
    input_box.delete("1.0", END)
    output_box.config(state=NORMAL)
    output_box.delete("1.0", END)
    output_box.config(state=DISABLED)

def copy_translation():
    output_text = output_box.get("1.0", END).strip()
    root.clipboard_clear()
    root.clipboard_append(output_text)
    root.update()

def record_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        input_box.delete("1.0", END)
        input_box.insert(END, "Listening...")
        root.update()
        try:
            audio = recognizer.listen(source, timeout=5)
            input_box.delete("1.0", END)
            text = recognizer.recognize_google(audio)
            input_box.insert(END, text)
        except sr.UnknownValueError:
            input_box.delete("1.0", END)
            input_box.insert(END, "Could not understand audio.")
        except sr.RequestError:
            input_box.delete("1.0", END)
            input_box.insert(END, "Speech recognition failed.")
        except sr.WaitTimeoutError:
            input_box.delete("1.0", END)
            input_box.insert(END, "Listening timed out.")

def speak_translation():
    output_text = output_box.get("1.0", END).strip()
    lang_code = LANGUAGES.get(target_lang.get(), 'hi')
    if output_text:
        try:
            tts = gTTS(text=output_text, lang=lang_code, slow=False)
            tts.save("temp.mp3")
            playsound.playsound("temp.mp3")
            os.remove("temp.mp3")
        except Exception as e:
            print("TTS Error:", e)


root = Tk()
root.title("Smart Translator")
root.geometry("600x800")
root.config(bg=LIGHT_BG)


title_label = Label(root, text="Smart Translator", font=("Segoe UI", 24, "bold"), bg=LIGHT_BG, fg=ACCENT)

source_lang = StringVar(value='Auto')
target_lang = StringVar(value='Hindi')

lang_frame = Frame(root, bg=LIGHT_BG)
source_dropdown = ttk.Combobox(lang_frame, textvariable=source_lang, values=list(LANGUAGES.keys()), width=20, state='readonly')
target_dropdown = ttk.Combobox(lang_frame, textvariable=target_lang, values=list(LANGUAGES.keys()), width=20, state='readonly')
source_dropdown.current(0)
target_dropdown.current(1)
source_dropdown.pack(side=LEFT, padx=10, pady=10)
target_dropdown.pack(side=LEFT, padx=10, pady=10)

input_label = Label(root, text="Enter text to translate", font=("Segoe UI", 14), bg=LIGHT_BG, fg=LIGHT_TEXT)
input_box = Text(root, font=("Segoe UI", 12), height=8, width=55, wrap=WORD, bd=2, relief=GROOVE, bg=LIGHT_TEXTBOX, fg=LIGHT_TEXT)

translate_btn = Button(root, text="Translate", command=translate_text, font=("Segoe UI", 12, "bold"), bg=ACCENT, fg="black", bd=0, relief=RIDGE, height=2, width=20)

button_frame = Frame(root, bg=LIGHT_BG)
clear_btn = Button(button_frame, text="Clear", command=clear_text, font=("Segoe UI", 10, "bold"), bg=ACCENT, fg="blue", relief=RIDGE, width=12)
copy_btn = Button(button_frame, text="Copy", command=copy_translation, font=("Segoe UI", 10, "bold"), bg=ACCENT, fg="blue", relief=RIDGE, width=12)
clear_btn.pack(side=LEFT, padx=10)
copy_btn.pack(side=LEFT, padx=10)

speech_btn_frame = Frame(root, bg=LIGHT_BG)
record_btn = Button(speech_btn_frame, text="🎤 Speak", command=record_speech, font=("Segoe UI", 10, "bold"), bg=ACCENT, fg="blue", relief=RIDGE, width=12)
speak_btn = Button(speech_btn_frame, text="🔊 Listen", command=speak_translation, font=("Segoe UI", 10, "bold"), bg=ACCENT, fg="blue", relief=RIDGE, width=12)
record_btn.pack(side=LEFT, padx=10)
speak_btn.pack(side=LEFT, padx=10)

output_label = Label(root, text="Translation", font=("Segoe UI", 14), bg=LIGHT_BG, fg=LIGHT_TEXT)
output_box = Text(root, font=("Segoe UI", 12), height=8, width=55, bg=LIGHT_TEXTBOX, fg=LIGHT_TEXT, wrap=WORD, state=DISABLED, bd=2, relief=GROOVE)

toggle_btn = Button(root, text="Switch to Dark Mode", command=toggle_theme, font=("Segoe UI", 10, "bold"), bg=ACCENT, fg="blue", relief=RIDGE)
footer_label = Label(root, text="Thank you", font=("Segoe UI", 10), bg=LIGHT_BG, fg=LIGHT_TEXT)


title_label.pack(pady=(30, 10))
lang_frame.pack()
input_label.pack(pady=(10, 5))
input_box.pack(pady=(0, 20))
translate_btn.pack(pady=10)
button_frame.pack(pady=10)
speech_btn_frame.pack(pady=10)
output_label.pack(pady=(20, 5))
output_box.pack()
toggle_btn.pack(pady=20)
footer_label.pack(side=BOTTOM, pady=10)


widgets = [
    title_label, input_label, output_label, footer_label,
    input_box, output_box, source_dropdown, target_dropdown,
    clear_btn, copy_btn, record_btn, speak_btn
]


root.mainloop()



