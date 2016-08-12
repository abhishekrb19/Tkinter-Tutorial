from Tkinter import *

root = Tk()

# grid is rows and cols
# you can put widgets into this grid (row, col) coordinate
# this saves a bit of confusion by avoiding side=LEFT/ BOTTOM ...

label1 = Label(root, text="Enter src bin")
label2 = Label(root, text="Enter dst bin")

# Note: pack will not be used here (if grid is used -- they are canonical to one another)!
# Pack and grid kinda does the same functionality -- they add the widgets into
# the window. Grid works w/ co-ordinates while pack works with side=LEFT, TOP ...

label1.grid(row=0,column=0) # @args: row, column
label2.grid(row=1, column=0)


root.mainloop()