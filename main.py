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
        print("You learnt all these French Words!")
        print('Starting Your Tutorial Again...')
        data = pandas.read_csv('data/french_words.csv')
        data = data.to_dict(orient='records')
        word_generate()
    return word_dict


def flip_card_now():
    canvas.itemconfig(image, image=front_image)
    canvas.itemconfig(title, text='French', fill="white")
    new_french_word = word_generate()['French']
    canvas.itemconfig(word, text=new_french_word, fill="white")

    right_button["state"] = "disabled"
    wrong_button["state"] = "disabled"
    
    window.after(3000, flip_card)
    
def right():
    data.pop(index)
    update()
    flip_card_now()

def wrong():
    flip_card_now()


def flip_card():
    canvas.itemconfig(image, image=back_image)
    canvas.itemconfig(title, text="English", fill="black")
    canvas.itemconfig(word, text=word_dict["English"], fill="black")
    
    right_button["state"] = "normal"
    wrong_button["state"] = "normal"


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
try:
    window.attributes('-zoomed', True)
except:
    window.state('zoomed')
window.title('Flashing Card')

canvas = Canvas(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
front_image = PhotoImage(file='images/card_back.png')
back_image = PhotoImage(file='images/card_front.png')

image = canvas.create_image(400, 263, image=front_image)

title = canvas.create_text(400, 150, text='French', font=('Arial', 30, 'italic'))
word = canvas.create_text(400, 263, text=word_generate()['French'], font=('Arial', 60, 'bold'))
    
canvas.place(relx = 0.5, rely=0.01, anchor=N)


wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, height=99, width=100, highlightthickness=0, border=0, command=wrong)
wrong_button.place(relx = 0.25, rely=0.88, anchor=N)

right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, height=99, width=100, highlightthickness=0, border=0, command=right)
right_button.place(relx = 0.75, rely=0.88, anchor=N)


flip_card_now()

window.mainloop()
