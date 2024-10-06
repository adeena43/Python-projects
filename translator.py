from tkinter import *
from tkinter import ttk
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import uuid
from playsound import playsound

def change(text="type", src="English", dest="Urdu"):
    text1 = text
    src1= src
    dest1 = dest
    trans = Translator()
    trans1 = trans.translate(text, src=src1, dest=dest1)
    return trans1.text

def data():
    s = comb_sor.get()
    d= comb_dest.get()
    message = sor_txt.get(1.0, END)
    text_get = change(text = message, src = s, dest = d)
    dest_txt.delete(1.0, END)
    dest_txt.insert(END, text_get)

def speak():
    text_to_speak = dest_txt.get(1.0, END).strip()
    if text_to_speak:
        language_name = comb_dest.get().lower()
        language_code = None

        for code, name in LANGUAGES.items():
            if name.lower() == language_name:
                language_code = code
                break

        if language_code:
            # Generate a unique filename for the speech file
            unique_filename = f"speech_{uuid.uuid4()}.mp3"
            
            # Use gTTS to convert the text to speech
            tts = gTTS(text=text_to_speak, lang=language_code)
            tts.save(unique_filename)
            
            # Play the saved speech file in the background
            playsound(unique_filename)

            # Optionally, delete the file afterward to avoid clutter (you can comment this out if you want to keep the files)
            os.remove(unique_filename)
        else:
            print(f"Language '{comb_dest.get()}' not found")

    else:
        print("No text to speak")

root = Tk()
root.title("Translator")
root.geometry("500x700")
root.config(bg = 'Pink')
lab_text = Label(root, text = "Translator", font=("Time New Roman", 40, "bold"))
lab_text.place(x = 100, y = 40, height = 50, width = 300)

frame = Frame(root).pack(side = BOTTOM)

lab_text = Label(root, text = "Text to Translate...", font=("Time New Roman", 20, "bold"), fg = "Black", bg = "Pink")
lab_text.place(x = 100, y = 100, height = 20, width = 300)

sor_txt = Text(frame, font = ("Time New Roman", 20, "bold"), wrap = WORD)
sor_txt.place(x = 10, y = 130, height = 150, width = 480)

list_txt = list(LANGUAGES.values())

comb_sor = ttk.Combobox(frame, value = list_txt)
comb_sor.place(x=10, y=300, height = 40, width=150)
comb_sor.set("English")

button_change = Button(frame, text="Translate", relief=RAISED, command= data)
button_change.place(x=170, y=300, height = 40, width = 150)

comb_dest = ttk.Combobox(frame, value = list_txt)
comb_dest.place(x=330, y=300, height = 40, width=150)
comb_dest.set("Urdu")

lab_text = Label(root, text = "Translated Text...", font=("Time New Roman", 20, "bold"), fg = "Black", bg = "Pink")
lab_text.place(x = 100, y = 360, height = 20, width = 300)

dest_txt = Text(frame, font = ("Time New Roman", 20, "bold"), wrap = WORD)
dest_txt.place(x = 10, y = 400, height = 150, width = 480)

button_speak = Button(frame, text="Speak", relief=RAISED, command=speak)
button_speak.place(x=170, y=580, height=40, width=150)


root.mainloop()
