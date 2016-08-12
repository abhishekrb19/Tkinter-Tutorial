from Tkinter import *

# Entry are Text Boxes!

root = Tk()

srcbin_label = Label(root, text="Enter the SRC bin to filter: ")
srcbin_label.grid(row=0, column=0,sticky="E") # sticky is used to alignment and E
# denotes right align!

srcbin_entry = Entry(root)
srcbin_entry.grid(row=0, column=1)


dstbin_label = Label(root, text="Enter the DST bin to filter and for viewing: ")
dstbin_label.grid(row=1, column=0,sticky="E")

dstbin_entry = Entry(root)
dstbin_entry.grid(row=1, column=1)

cbutton = Checkbutton(root,text="Remember me")
cbutton.grid(columnspan=2,sticky="E")

root.mainloop()