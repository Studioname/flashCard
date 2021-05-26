from tkinter import *
import pandas
from random import choice, randint
BACKGROUND_COLOR = "#B1DDC6"
card = None
timer = None

try:
    file = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    file = pandas.read_csv("./data/french_words.csv")

dictionary_pairs = pandas.DataFrame.to_dict(file, orient="records")

#---------------------------------------------FUNCTIONS----------------------------------------------------------------#


def get_card():
    global card, timer
    card = choice(dictionary_pairs)
    french_word = card["French"]
    canvas.itemconfig(card_image, image=card_picture_front)
    canvas.itemconfig(language_text, text=french_word,fill="black")
    canvas.itemconfig(language_label, text="French", fill="black")
    timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_image,image=card_picture_back)
    canvas.itemconfig(language_label, text="English",fill="white")
    canvas.itemconfig(language_text, text=card["English"],fill="white")


def right_button_pressed():
    try:
        pandas.read_csv("words_to_learn.csv")
    except FileNotFoundError:
        words_to_learn = dictionary_pairs
        data = pandas.DataFrame(words_to_learn)
        data.to_csv("words_to_learn.csv")
    else:
        global card
        dictionary_pairs.remove(card)
        words_to_learn = dictionary_pairs
        data = pandas.DataFrame(words_to_learn)
        data.to_csv("words_to_learn.csv",index=False)
    finally:
        window.after_cancel(timer)
        get_card()


def wrong_button_pressed():
    window.after_cancel(timer)
    get_card()

#---------------------------------------------UI STUFF-----------------------------------------------------------------#

window = Tk()

window.title("Flashy")
window.config(padx=50,pady=50, bg="powderblue")

card_picture_front = PhotoImage( file="./images/card_front.png", )
card_picture_back = PhotoImage( file="./images/card_back.png")

#0,0

canvas = Canvas(width=800,height=526)
card_image = canvas.create_image(400, 263, image=card_picture_front)
canvas.config(bg="powderblue", highlightthickness = 0)
language_label = canvas.create_text(400,150, font=("Ariel", 40, "italic"),text="")
language_text = canvas.create_text(400, 263, font=("Ariel", 60, "bold"), text="")

canvas.grid(column=0,row=0, columnspan=2)

#0,1
wrong_button_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=wrong_button_pressed)
wrong_button.config(highlightthickness=0)
wrong_button.grid(column=0,row=1)

#0,2
right_button_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, command=right_button_pressed)
right_button.config(highlightthickness=0)
right_button.grid(column=1,row=1)

get_card()
window.mainloop()


