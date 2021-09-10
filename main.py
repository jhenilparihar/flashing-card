from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
word_dict = {}
index = 0

try:
    data = pandas.read_csv('data/word_to_learn.csv')
    data = data.to_dict(orient='records')
except FileNotFoundError:
    data = pandas.read_csv('data/french_words.csv')
    data = data.to_dict(orient='records')
except pandas.errors.EmptyDataError:
    data = pandas.read_csv('data/french_words.csv')
    data = data.to_dict(orient='records')


def update():
    file = pandas.DataFrame(data)
    file.to_csv('data/word_to_learn.csv', index=False)


def word_generate():
    global word_dict, index, data
    try:
        index = random.randint(0, len(data))-1
        word_dict = data[index]
    except IndexError:
        print('Starting Your Tutorial Again')
        data = pandas.read_csv('data/french_words.csv')
        data = data.to_dict(orient='records')
        word_generate()
    return word_dict


def right():
    data.pop(index)
    update()

    canvas.itemconfig(image, image=front_image)
    canvas.itemconfig(title, text='French', fill="black")
    new_french_word = word_generate()['French']
    canvas.itemconfig(word, text=new_french_word, fill="black")

    window.after(3000, flip_card)


def wrong():
    canvas.itemconfig(image, image=front_image)
    canvas.itemconfig(title, text='French', fill="black")
    new_french_word = word_generate()['French']
    canvas.itemconfig(word, text=new_french_word, fill="black")

    window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(image, image=back_image)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=word_dict["English"], fill="white")


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title('Flashing Card')

canvas = Canvas(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
front_image = PhotoImage(file='images/card_front.png')
back_image = PhotoImage(file='images/card_back.png')

image = canvas.create_image(400, 263, image=front_image)

title = canvas.create_text(400, 150, text='French', font=('Arial', 30, 'italic'))
word = canvas.create_text(400, 263, text=word_generate()['French'], font=('Arial', 60, 'bold'))

window.after(3000, flip_card)

canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, height=99, width=100, highlightthickness=0, border=0, command=wrong)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, height=99, width=100, highlightthickness=0, border=0, command=right)
right_button.grid(column=1, row=1)

window.mainloop()
