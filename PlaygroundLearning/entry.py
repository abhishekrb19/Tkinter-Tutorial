from Tkinter import *

# Entry are Text Boxes!

root = Tk()


def evaluate(val):
    print "entered value:", srcbin_entry.get() # data from the Entry / Textbox!


srcbin_label = Label(root, text="Enter the src bin to filter: ")
srcbin_label.grid(row=0, column=0)

srcbin_entry = Entry(root)
srcbin_entry.grid(row=0, column=1)
srcbin_entry.bind("<Return>",evaluate)

# srcbin_entry.pack()


root.mainloop()