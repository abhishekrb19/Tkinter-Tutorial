import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt # TODO(abhishek): consider removing pyplot and just stick w/ matplotlib
# Check: http://stackoverflow.com/questions/25839795/opening-a-plot-in-tkinter-only-no-matplotlib-popup
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk
# import Tkinter.ttk as ttk
import sys
import numpy as np
from matplotlib.gridspec import GridSpec

import multiprocessing
from multiprocessing import Process, Queue
import capnp
import ip_proto_capnp
import custom_config
import logging
import gflags
import Tkinter
from Tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Grid Manager")

        for r in range(6):
            self.master.rowconfigure(r, weight=1)    
        for c in range(5):
            self.master.columnconfigure(c, weight=1)
            Button(master, text="Button {0}".format(c)).grid(row=6,column=c,sticky=E+W)

        Frame1 = Frame(master, bg="red")
        Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 
        Frame2 = Frame(master, bg="blue")
        Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        Frame3 = Frame(master, bg="green")
        Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)

        self.fig = plt.figure(figsize=(10,10))
        # ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        self.gs = GridSpec(3,1)
        ax = self.fig.add_subplot(self.gs[0:2,:])
        # self.im = ax.imshow(-np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest', vmax=0, vmin=-400000)
        #
        self.canvas = FigureCanvasTkAgg(self.fig, master=Frame3)
        # self.canvas.show()
        # self.canvas.get_tk_widget().grid(side='top', fill='both', expand=1)
        self.canvas.get_tk_widget().grid()




        # # self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        # self.canvas.get_tk_widget().grid(row=0,column=1)
        # #toolbar = NavigationToolbar2TkAgg(self.canvas, master)
        # #toolbar.update()
        # self.canvas._tkcanvas.pack(side='top')



        #frame.pack()


root = Tk()
app = Application(master=root)
root.geometry("400x200+200+200")
app.mainloop()