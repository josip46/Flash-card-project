from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
random_numb = 0

window = Tk()
window.title('Flashy')
window.config(padx=100, pady=100, bg=BACKGROUND_COLOR)

# Read from csv
try:
    data_frame = pandas.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    original_data_frame = pandas.read_csv('./data/french_words.csv')
    word_to_learn = original_data_frame.to_dict(orient='records')
else:
    word_to_learn = data_frame.to_dict(orient='records')
current_card = {}

# Back of the card
card_image_back = PhotoImage(file='./images/card_back.png')


# Changing card
def change_card():
    global current_card
    canvas.itemconfig(image_cont, image=card_image_back)
    canvas.itemconfig(title_text, text='English', fill='white')
    canvas.itemconfig(word_text, text=current_card['English'], fill='white')


def random_word():
    # Button press creates random French word
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(word_to_learn)
    canvas.itemconfig(title_text, text='French', fill='black')
    canvas.itemconfig(word_text, text=current_card['French'], fill='black')
    canvas.itemconfig(image_cont, image=card_image_front)
    flip_timer = window.after(3000, change_card)


def is_known():
    word_to_learn.remove(current_card)
    data = pandas.DataFrame(word_to_learn)
    data.to_csv('./data/words_to_learn.csv', index=False)
    random_word()


flip_timer = window.after(3000, change_card)
# Canvas
canvas = Canvas(width=800, height=562, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image_front = PhotoImage(file='./images/card_front.png')
image_cont = canvas.create_image(400, 281, image=card_image_front)
title_text = canvas.create_text(400, 150, text="", fill='black', font=('Arial', 30, 'italic'))
word_text = canvas.create_text(400, 270, text="", fill='black', font=('Arial', 35, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

# We call the function to have a random French word at the start screen
random_word()

# Buttons
wrong_button_image = PhotoImage(file='./images/wrong.png')
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=random_word)
wrong_button.grid(row=1, column=0)
right_button_image = PhotoImage(file='./images/right.png')
right_button = Button(image=right_button_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

window.mainloop()
