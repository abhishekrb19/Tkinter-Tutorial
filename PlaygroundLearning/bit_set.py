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
from bitarray import bitarray



class AMON_App(Frame):


    def __init__(self, master=None, data_queue=None, interactive_filter_queue=None):
        Frame.__init__(self, master)
        self.data_queue = data_queue
        self.interactive_filter_queue = interactive_filter_queue
        self.create_widgets()
        self.create_graphs()
        self.pack(fill='both', expand=True)


    def create_widgets(self):
        # Frame that resides on the left side of the window
        self.widgets_frame = Frame(self)
        self.widgets_frame.pack(side='left', padx=10, pady=10, fill='both')

        # Source bucket widgets
        # self.label_src = Label(master=self.widgets_frame, text="Enter the src bin to filter: ", font=('bold'))
        # self.label_src.grid(sticky=W)
        # self.entry_src = Entry(master=self.widgets_frame)
        # self.entry_src.grid(sticky=W)
        # self.entry_src.bind("<Return>",self.evaluate_src)


        # Destination bucket widgets
        self.label_dst = Label(master=self.widgets_frame, text="Enter the dst bin to filter: ", font=('bold'))
        self.label_dst.grid(sticky=W)
        self.entry_dst = Entry(master=self.widgets_frame)
        self.entry_dst.grid(sticky=W)
        # self.entry_dst.bind("<Return>",self.evaluate_dst)
        self.entry_dst.bind("<Return>",self.parse_bins_from_dst_entry_box)

        # Button widget that handles both source and destination widgets
        self.button = Button(master=self.widgets_frame, text="Click to Filter!")
        self.button.bind("<Button-1>",self.evaluate_src_dst) # Binding event -- Button 1 (left mouse click)!
        self.button.grid(sticky=W)

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
        self.im = ax.imshow(-np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest', vmax=0, vmin=-400000)


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

        proto_obj = self.data_queue.get()
        if  proto_obj[0].size == 0:

            root.after(1000, self.refresher)
        else:
            # databrick sketch
            num_intensities = proto_obj[0].reshape(128,128)
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
            root.after(1000, self.refresher) # every second...



    def evaluate_src_dst(self, event):
        # logging.info("Filtering Src and Dst bins:%d and %d"%(self.entry_src.get(), self.entry_dst.get()))
        logging.info("Filtering Src and Dst bins:%d and %d"%(0, int(self.entry_dst.get())))
        #filter_src_bin = int(self.entry_src.get())
        filter_dst_bin = int(self.entry_dst.get())
        self.interactive_filter_queue.put(filter_dst_bin)

    def evaluate_src(self,val):
        #logging.info("Filtering Src bin value:%d"%int(self.entry_src.get()))
        #filter_src_bin = int(self.entry_src.get())
        logging.warn("Sorry, this textbox is not configured yet!")

    def evaluate_dst(self,val):
        logging.warn("Filtering Dst bin value:%d"%int(self.entry_dst.get()))
        filter_dst_bin = int(self.entry_dst.get())
        bins = bitarray(128)
        bins.setall(0)
        bins[filter_dst_bin] = 1
        # TODO(abhishek): Here we will have to get multiple bins and put them into the bitmap

        consolidated_bins = self.shifting(bins)
        logging.warn("Entered Consolidated into Queue:%d"%consolidated_bins)
        self.interactive_filter_queue.put(consolidated_bins)

    def parse_bins_from_dst_entry_box(self, val):
        bins = bitarray(128)
        bins.setall(0)
        string = self.entry_dst.get()

        logging.warn("Entered string was: %s"%string)
        split_bins_list = string.split(" ")
        if int(split_bins_list[0]) == -1:
            logging.warn("EXPLICIT Entered Consolidated into Queue:%d"%-1)
            self.interactive_filter_queue.put(-1)
        else:
            for each_bin in split_bins_list:
                bins[int(each_bin)] = 1

            consolidated_bins = self.shifting(bins)
            logging.warn("Entered Consolidated into Queue:%d"%consolidated_bins)
            self.interactive_filter_queue.put(consolidated_bins)


    def shifting(self, bitlist):
        out = 0
        for bit in reversed(bitlist):
            out = (out << 1) | bit
        return out


class FlowtransmitImpl(ip_proto_capnp.Flowtransmit.Server):
    "Implementation of Flow Transmit Interface in the schema file"
    def __init__(self):
        self.sent_bin = None
        self.already_sent = False

    def src(self, databrick, hitters, _context, **kwargs):

        np_databrick = np.array(databrick)
        #print np_databrick

        #print np_databrick[0]
        count_zeros = 0
        for d in range(len(np_databrick)):
            if np_databrick[d] == 0:
                count_zeros += 1


        logging.info("# of zeros :%d, max: %d, min: %d"%(count_zeros, max(np_databrick), min(np_databrick)))

        src_hitters_li = []
        dst_hitters_li = []
        hitter_bytes = []

        for h in hitters:
            src_hitters_li.append(h.ipsrc)
            dst_hitters_li.append(h.ipdst)
            hitter_bytes.append(h.bytes)

        logging.info("Putting data brick and hitters in the shared process queue")

        data_queue.put((np_databrick, src_hitters_li, dst_hitters_li, hitter_bytes))

        try:
            filter_bin = interactive_filter_queue.get(block = False)
            logging.warn("filter bin entered: %d",int(filter_bin))
            self.sent_bin = int(filter_bin)
            return int(filter_bin)
        except:

            if not self.sent_bin:
                logging.warn("Nothing was entered")
                return 0
            else:
                return int(self.sent_bin)

def listen_conn_process(data_queue, interactive_filter_queue, port_number):
    address = "*:"+ str(port_number)
    already_sent = False
    sent_bin = None
    server = capnp.TwoPartyServer(address,bootstrap=FlowtransmitImpl())
    custom_config.ConfigLoggerAndFlags()
    logging.info("Listening to Incoming connections on port:%d"%port_number)
    server.run_forever()



if __name__ == '__main__':
    FLAGS = gflags.FLAGS
    capnp.remove_import_hook()
    gflags.DEFINE_string('port', 8000, 'Port number to bind the socket to (Default:8000)')

    port_number = int(FLAGS.port)
    custom_config.ConfigLoggerAndFlags()

    manager = multiprocessing.Manager()
    data_queue = manager.Queue()

    #interactive_filter_queue = manager.Queue()
    interactive_filter_queue = Queue()

    cap_conn_process = Process(target=listen_conn_process, args=(data_queue,interactive_filter_queue, port_number))
    cap_conn_process.start()
    logging.info("Cap'n Proto process started on port:%d"%port_number)

    root = Tk()
    app = AMON_App(master=root, data_queue=data_queue,interactive_filter_queue=interactive_filter_queue)
    root.title("AMON Viz")
    app.refresher()
    app.mainloop()
