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
        self.master.title("AMON Visualization")

        # for r in range(12):
        #     self.master.rowconfigure(r, weight=1)
        # for c in range(10):
        #     self.master.columnconfigure(c, weight=1)
            # Button(master, text="Button {0}".format(c)).grid(row=6,column=c,sticky=E+W)

        # Frame1 = Frame(master, bg="red")
        # Frame1.grid(row = 0, column = 0, rowspan = 19, columnspan = 2, sticky = W+E+N+S)
        Frame2 = Frame(master, bg="blue")
        #Frame2.grid(row = 0, column = 0, rowspan = 10, columnspan = 10, sticky = W+E+N+S)
        Frame2.pack(side = LEFT, fill = BOTH)

        # Frame2.grid(row = 0, column = 0)
        Frame3 = Frame(master, bg= "red")
        #Frame3.grid(row = 10, column = 0, rowspan = 2, columnspan = 10, sticky = W+E+N+S)
        Frame3.pack(side = RIGHT, fill=BOTH)
        # Frame3.grid(row = 10, column = 0)

        # Fig1 and canvas1
        self.fig1 = plt.figure(figsize=(7,7))
        # self.gs = GridSpec(3,1)
        self.gs1 = GridSpec(2,1)
        ax = self.fig1.add_subplot(self.gs1[0:2,:])
        # ax = self.fig.add_subplot(111)
        self.im = ax.imshow(-np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest', vmax=0, vmin=-400000)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=Frame3)
        toolbar = NavigationToolbar2TkAgg(self.canvas1, Frame3)
        toolbar.update()
        # toolbar.update()
        # self.canvas1._tkcanvas.pack(side='top')

        self.gs2 = GridSpec(2,1)
        self.fig2 = plt.figure(figsize=(5,5))
        self.topkplot = self.fig2.add_subplot(self.gs2[0:2,:])
        self.topkplot.set_title('Top K hitters Stats')
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=Frame3)

        # self.canvas.get_tk_widget().grid(row=0,column=1)

        # toolbar.update()
        self.canvas1._tkcanvas.pack(side='top')
        self.canvas2._tkcanvas.pack(side='bottom')

        Frame3.pack()

        # self.label_src = Tkinter.Label(master=Frame2, text="Enter the src bin to filter: ")
        # self.label_src.grid(row=0, column=0)
        # self.label_src.pack(side="left")

        # self.entry_src = Tkinter.Entry(Frame2)
        # # self.entry_src.pack(side="right")
        # self.entry_src.grid(row=0, column=1)
        # self.entry_src.bind("<Return>",self.evaluate)
        #
        # self.label_dst = Tkinter.Label(master=Frame2, text="Enter the dst bin to filter: ")
        # self.label_dst.grid(row=0, column=2)
        # # self.label_src.pack(side="left")
        #
        # self.entry_dst = Tkinter.Entry(Frame2)
        # # self.entry_src.pack(side="right")
        # self.entry_dst.grid(row=0, column=3)
        # self.entry_dst.bind("<Return>",self.evaluate)
        # Frame2.pack()

    def evaluate(self,val):
        print "entered value:", self.entry_src.get() # data from the Entry / Textbox!
        filter_bin = self.entry_src.get()



root = Tk()
app = Application(master=root)
root.geometry("900x900+200+200")
app.mainloop()