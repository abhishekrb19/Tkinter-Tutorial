from Tkinter import *
import Tkinter as Tk
import matplotlib
matplotlib.use("TkAgg") #http://stackoverflow.com/questions/32019556/matplotlib-crashing-tkinter-application
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.gridspec import GridSpec
from pylab import rcParams

# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from numpy import arange, sin, pi
import numpy as np

root = Tk.Tk()


pause = False

def onClick(event):
    global pause
    pause ^= True
    #logging.warn("Paused!!%s"%pause)
    print "Pasue status:",pause


# plt.ion()
gs=GridSpec(3,1) # 3 rows, 1 column
# rcParams['figure.figsize'] = 20, 10
# fig = plt.figure()

fig = Figure(figsize=(5, 4), dpi=100)
# a = f.add_subplot(111)

ax = fig.add_subplot(gs[0:2,:])

# plt.title('Databricks Visualization')


t = arange(0.0, 3.0, 0.01)
s = sin(2*pi*t)

# ax.plot(t, s)



canvas = FigureCanvasTkAgg(fig, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

canvas.set_window_title('AMON')
canvas.mpl_connect('button_press_event', onClick)
canvas.show()
# using evaluate built-in function-- taken in an expression and evaluates it!

def evaluate(event):
    data = e.get()
    print data


e = Entry(root)
e.bind("<Return>", evaluate)
e.pack()

while True:
    im = ax.imshow(np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest', vmax = 0, vmin = -400000)




root.mainloop()