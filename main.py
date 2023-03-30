from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/portuguese_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# -------------------------------- Create New Flash Cards -------------------------------- #


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title, text="Portuguese", fill="black")
    canvas.itemconfig(word, text=current_card["Portuguese"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# ------------------------------- Save Checked Words To CSV ------------------------------ #


def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# --------------------------------------- UI DESIGN -------------------------------------- #
window = Tk()
window.title("English/Portuguese Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images\card_front.png")
card_back_img = PhotoImage(file="images\card_back.png")
card_background = canvas.create_image(400, 265, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)
title = canvas.create_text((400, 150), text="Portuguese", fill="black", font=("Ariel", 40, "italic"))
word = canvas.create_text((400, 263), text="Word", fill="black", font=("Ariel", 60, "bold"))

x_btn_img = PhotoImage(file="images/wrong.png")
x_btn = Button(image=x_btn_img, highlightthickness=0, command=next_card)
x_btn.grid(column=0, row=1)

check_btn_img = PhotoImage(file="images/right.png")
check_btn = Button(image=check_btn_img, highlightthickness=0, command=is_known)
check_btn.grid(column=1, row=1)

next_card()
window.mainloop()
