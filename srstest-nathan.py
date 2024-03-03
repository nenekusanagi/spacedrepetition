from tkinter import *
window = Tk()
window.title("Spaced Repetition Flashcard Software")
window.iconbitmap("librarypc.ico")
window.geometry("640x480")

title = Label(text="Spaced Repetition Flashcard Software",anchor=CENTER,bg="grey",cursor="heart",font=("arial",20,"underline"),fg="black",height=5,justify=RIGHT,padx=30)
title.pack()

window.mainloop()