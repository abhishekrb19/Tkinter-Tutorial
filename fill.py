from Tkinter import *

root =Tk()

# screens are re-sizeable
# but the widgets aren't!

# So if you want to resize the widgets as well as the size of the
# window grows/shrinks.

play_button = Button(None, text="Pause")
stop_button = Button(None, text="Play")

play_button.pack(fill=X)
stop_button.pack(fill=Y)
root.mainloop()