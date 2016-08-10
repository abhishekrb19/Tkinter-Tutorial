from Tkinter import *

def toggle():
    i = 1
    b = 2
    print(i, b)
    pass

root = Tk()
frame = Frame(root, width=100, height=100)
button = Button(frame,text="Press", command=toggle).grid(column=1, row=1)
frame.pack()
root.mainloop()