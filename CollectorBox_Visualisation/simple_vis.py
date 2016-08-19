__author__ = 'Abhishek'
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
# import ip_proto_capnp
import ip_proto_list_capnp
import custom_config
import logging
import gflags
import Tkinter
from Tkinter import *
from bitarray import bitarray
# import warnings
import subprocess, signal, os






gflags.DEFINE_string('port', 8000, 'Port number to bind the socket to (Default:8000)')
custom_config.ConfigLoggerAndFlags()
logging.info("Setting up the GFLAGS config")
FLAGS = gflags.FLAGS
capnp.remove_import_hook()
port_number = int(FLAGS.port)


class AMON_App(Frame):


    def __init__(self, master=None, data_queue=None, interactive_filter_queue=None):
        Frame.__init__(self, master)
        self.data_queue = data_queue
        self.interactive_filter_queue = interactive_filter_queue
        self.create_widgets()
        self.create_graphs()
        self.pack(fill='both', expand=True)
        self.play_pause = True # True (play), False (pause)

        self.src_int_bin_map = [0]*128 #to mimic 128 bitmap for src bins faster table lookups
        self.dst_int_bin_map = [0]*128 #to mimic 128 bitmap for dst bins faster table lookups

    def create_widgets(self):
        # Frame that resides on the left side of the window
        self.widgets_frame = Frame(self)
        self.widgets_frame.pack(side='left', padx=10, pady=10, fill='both')



        # Destination bucket widgets
        self.label_dst = Label(master=self.widgets_frame, text="Enter the src bin to filter: ", font=('bold'))
        self.label_dst.grid(sticky=W)
        self.entry_dst = Entry(master=self.widgets_frame)
        self.entry_dst.grid(sticky=W)
        # self.entry_dst.bind("<Return>",self.evaluate_dst)


        # Source bucket widgets
        self.label_src = Label(master=self.widgets_frame, text="Enter the dst bin to filter: ", font=('bold'))
        self.label_src.grid(sticky=W)
        self.entry_src = Entry(master=self.widgets_frame)
        self.entry_src.grid(sticky=W)
        #self.entry_src.bind("<Return>",self.parse_bins_from_src_entry_box_into_intarray)


        #self.entry_dst.bind("<Return>",self.parse_bins_from_dst_entry_box_into_intarray)

        # Button widget that handles both source and destination widgets
        self.button = Button(master=self.widgets_frame, text="Click to Filter!")
        self.button.bind("<Button-1>",self.evaluate_src_dst) # Binding event -- Button 1 (left mouse click)!
        self.button.grid(sticky=W)

        # Add Pause/ Play button
        self.pause_button = Button(master=self.widgets_frame, text="Pause")
        self.pause_button.bind("<Button-1>",self.trigger_pause)
        self.pause_button.grid(sticky=W)

    def create_graphs(self):

        # Frame that resides on right side of window
        self.graphFrame = Frame(self)
        self.graphFrame.pack(side='right', fill='both', expand=True)
        Grid.rowconfigure(self.graphFrame, 0, weight=1)
        Grid.columnconfigure(self.graphFrame, 0, weight=1)

        # databricks visualization
        self.fig = plt.figure(figsize=(10,10))
        self.gs = GridSpec(3,1)
        ax = self.fig.add_subplot(self.gs[0:2,:])
        #self.im = ax.imshow(-np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest', vmax=0, vmin=-400000)
        self.im = ax.imshow(-np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest')


        # bar graph visualization
        self.num_graphed = 0
        self.topkplot = self.fig.add_subplot(self.gs[2,:])
        self.topkplot.set_title('Top K hitters Stats')

        # Canvas and Toolbar definitions for the graphs
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphFrame)
        self.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)
        toolbar = NavigationToolbar2TkAgg(self.canvas, self.graphFrame)
        toolbar.update()
        self.canvas._tkcanvas.pack(side='top', fill='both', expand=True)
        self.canvas.show()

    def refresher(self):

        if self.play_pause:

            try:
                proto_obj = self.data_queue.get(block=False)
                if  proto_obj[0].size == 0: # TODO(abhishek): Would control ever come here, since I added try-catch ?

                    # self.after(2000, self.refresher)
                    self.graphFrame.after(1000,self.refresher)
                else:
                    # databrick sketch
                    num_intensities = proto_obj[0].reshape(128,128)
                    logging.info("databrick intensities:%s",num_intensities)
                    self.im.set_array(-num_intensities)

                    combined = []
                    for idx, src in enumerate(proto_obj[1]):
                        combined.append(src + "\n - \n" + proto_obj[2][idx])
                    y_pos = np.arange(len(combined))

                    #TODO(abhishek): Push this to below ==0: block (to avoid re-drawing all the time)?


                    if self.num_graphed == 0:
                        self.bar_rect = plt.bar(y_pos, proto_obj[3], align='center', alpha=0.3, width=0.2, color='maroon')
                        self.num_graphed += 1
                    else:

                        for i in range(len(combined)):
                            for rect, h in zip(self.bar_rect, proto_obj[3]):
                                rect.set_height(h)

                    plt.xticks(y_pos, combined)
                    plt.ylabel('# of Bytes')
                    plt.xlabel('Top %d hitters (src ip - dst ip)' %len(combined))
                    self.canvas.draw()
                    # self.after(2000, self.refresher) # every second...
                    self.graphFrame.after(1000,self.refresher)
            except:
                logging.info("Empty exception as queue")
                self.graphFrame.after(1000, self.refresher)
        else:
            self.graphFrame.after(1000, self.refresher)



    def evaluate_src_dst(self, event):
        # logging.info("Filtering Src and Dst bins:%d and %d"%(0, int(self.entry_dst.get())))
        #filter_src_bin = int(self.entry_src.get())

        # filter_dst_bin = int(self.entry_dst.get())
        # self.interactive_filter_queue.put(filter_dst_bin)

        string_src = self.entry_src.get()
        string_dst = self.entry_dst.get()
        logging.warn("Entered string for src and dst are: %s, %s"%(string_src, string_dst))

        split_bins_list_src = string_src.split(" ")
        split_bins_list_dst = string_dst.split(" ")

        # Source text box processing follows here
        if int(split_bins_list_src[0]) == -1:
            self.src_int_bin_map[0] = 2
            logging.warn("Clearing src bin by setting it to: %d"%2)

            #self.interactive_filter_queue.put(self.src_int_bin_map)
        else:
            for bin in split_bins_list_src:
                bin = int(bin)
                self.src_int_bin_map[bin] = 1

            logging.warn("Src bin processing done: %s"%self.src_int_bin_map)
            #self.interactive_filter_queue.put(self.src_int_bin_map)

        # Destination text box processing follows here
        if int(split_bins_list_dst[0]) == -1:
            self.dst_int_bin_map[0] = 2
            logging.warn("Clearing dst bin by setting it to::%d"%2)

            #self.interactive_filter_queue.put(self.dst_int_bin_map)
        else:
            for bin in split_bins_list_dst:
                bin = int(bin)
                self.dst_int_bin_map[bin] = 1

            logging.warn("Dst bin processing done: %s"%self.dst_int_bin_map)
            #self.interactive_filter_queue.put(self.dst_int_bin_map)

        logging.warn("Inserting the src and dst bin filter lists into queue")
        self.interactive_filter_queue.put((self.src_int_bin_map,self.dst_int_bin_map))
        # clear the map now
        logging.warn("Clearing the 128 byte char maps for src and dst filter bins now!")
        self.src_int_bin_map = [0]*128
        self.dst_int_bin_map = [0]*128


    def trigger_pause(self,event_click):
        self.play_pause ^= True
        if self.play_pause:
            self.pause_button.config(text="Pause")
        else:
            self.pause_button.config(text="Play")

def signal_handler(_, __):

    logging.critical("You pressed Ctrl + C / Ctrl + Z to terminate the program")
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    pids = []
    logging.info("Killing this running script: %s"%__file__)
    for line in out.splitlines():
        if __file__ in line:
            pid = int(line.split(None, 1)[0])
            pids.append(pid)

    logging.critical("Killing Parent and Child processes")
    logging.info("Killing Child Process with pid: %d"%pids[-1])
    os.kill(pids[-1], signal.SIGKILL)
    logging.info("Killing Parent Process with pid: %d"%pids[0])
    os.kill(pids[0], signal.SIGKILL)

if __name__ == '__main__':

    manager = multiprocessing.Manager()
    data_queue = manager.Queue()

    #interactive_filter_queue = manager.Queue()
    interactive_filter_queue = Queue()


    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler) # Ctrl + C
    #signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler) # Ctrl + Z

    root = Tk()
    app = AMON_App(master=root, data_queue=data_queue,interactive_filter_queue=interactive_filter_queue)
    root.title("AMON Viz")
    app.refresher()
    app.mainloop()
