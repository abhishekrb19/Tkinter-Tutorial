__author__ = 'Abhishek'


try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter
except ImportError:
    # for Python3
    from tkinter import *   ## notice here too

root = Tk() # loads a minimal window with min, max, and close signs
root.mainloop() # this prevents the window from closing immediately until the user closes it manually


