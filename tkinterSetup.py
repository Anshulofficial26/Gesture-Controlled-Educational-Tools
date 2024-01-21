from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb
import os
from PIL import ImageTk, Image

def run1():
    os.system('python main.py')


def run2():
    os.system('python gestureQuiz.py')

root = tb.Window(themename="superhero")

root.title("JIIT Teachify")
root.geometry('1500x1200')
#root.iconbitmap('extras/jiit.png')

my_label = tb.Label(text="Gesture Controlled Education Tools", font=("Helvetica", 25), bootstyle = "danger,inverse")
my_label.pack(pady=60)


img = ImageTk.PhotoImage(Image.open("extras/jiit.png"))
my_Label = Label(image=img)
my_Label.pack(pady=30)

#button styles
my_style = tb.Style()
my_style.configure('success.TButton', font=("Helvetica", 15))

my_button = tb.Button(text="Gesture Quiz", bootstyle="success,outline",style="success.TButton", command=run2)
my_button.pack(pady=80)

my_button2 = tb.Button(text="Gesture Presentation", bootstyle="success,outline",style="success.TButton", command=run1)
my_button2.pack(pady=80)

#quit_button = tb.Button(text="Exit Program",bootstyle="success,outline", command=root.quit)
#quit_button.pack(pady=300)

root.mainloop()
