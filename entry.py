from Tkinter import *

# Entry are Text Boxes!

root = Tk()

srcbin_label = Label(root, text="Enter the src bin to filter: ")
srcbin_label.grid(row=0, column=0)

srcbin_entry = Entry(root)
srcbin_entry.grid(row=0, column=1)



root.mainloop()