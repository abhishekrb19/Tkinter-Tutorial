from Tkinter import *

root = Tk()

# create a label

name_label = Label(root, text="This is the tkinter window")

# you need to put the label into the window -- using pack

name_label.pack() # whenever you create any widget (label, button, etc),
# you need to pack into the window!

myname_label = Label(root, text="This is created by Abhishek")

myname_label.pack()

root.mainloop()