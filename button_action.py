#import Tkinter as tk
from Tkinter import *

root =  Tk()

def update_src_bin(e):
    print "updated!"

# Method 1:
update_button_bin = Button(root, text="Update src bin", command=update_src_bin)
update_button_bin.pack()


def method2(e):
    print ("Hello from second method!")

# Method 2:
# MOSTLY used approach
button2 = Button(root, text="Another button")
button2.bind("<Button-1>",method2) # Binding event -- Button 1 (left mouse click)!
button2.pack()


root.geometry("500x500")

# binding multiple events to a widget / window (like below)
root.bind("<Button-1>",update_src_bin)
root.bind("<Left>",method2)

root.mainloop()



