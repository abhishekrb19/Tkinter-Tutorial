from Tkinter import *

root = Tk()

my_button = Button(None, text="Pause!", fg="red") # @args: layout, text, fg (foreground -- text color)
# colors don't work in Mac strangely! Check SO
my_button.pack()

my_button = Button(None, text="Play!", fg="blue")
my_button.pack()

root.mainloop()