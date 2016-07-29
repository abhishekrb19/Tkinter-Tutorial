from Tkinter import *



root = Tk()

# we create frames to neatly group!
top_frame = Frame(root)
top_frame.pack()

bottom_frame = Frame(root)
bottom_frame.pack(side=BOTTOM) #Note we don't say side=TOP for top_frame(implicit)

pause_button = Button(top_frame, text="Pause")
pause_button.pack(side=RIGHT)

play_button = Button(top_frame, text="Play")
play_button.pack(side=RIGHT)

play_button = Button(bottom_frame, text="Misc1")
play_button.pack(side=LEFT)

play_button = Button(bottom_frame, text="Misc2")
play_button.pack(side=LEFT)

root.mainloop()