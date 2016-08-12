# https://gist.github.com/chappers/bd910bfb0ed73c509802
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

from Tkinter import Label, Entry

class App:
    def __init__(self, master=None, data_queue=None, interactive_filter_queue=None):
        # Create a container
        frame = Tkinter.Frame(master)
        self.num_graphed = 0
        self.data_queue = data_queue
        self.interactive_filter_queue = interactive_filter_queue
        # Create 2 buttons


        # create a label and an entry box
        # self.label_src = Tkinter.Label(master=frame, text="Enter the dst bin to filter: ")
        # self.label_src.grid(row=1, column=0)
        # # self.label_src.pack(side="left")
        #
        # self.entry_src = Tkinter.Entry(master=frame)
        # # self.entry_src.pack(side="right")
        # self.entry_src.grid(row=2, column=0)
        # self.entry_src.bind("<Return>",self.evaluate)

        # fig = Figure()
        self.button_left = Tkinter.Button(frame,text="< AAA ")
        self.button_left.pack(side="bottom")
        self.button_left.grid(row = 0, column = 0)
        self.button_right = Tkinter.Button(frame,text="BBB  >")
        # self.button_right.pack(side="bottom")
        self.button_right.grid(row = 0, column = 1)
        self.fig = plt.figure(figsize=(10,10))
        # ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        self.gs = GridSpec(3,1)
        ax = self.fig.add_subplot(self.gs[0:2,:])
        self.im = ax.imshow(-np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest', vmax=0, vmin=-400000)

        self.num_graphed = 0
        self.topkplot = self.fig.add_subplot(self.gs[2,:])
        self.topkplot.set_title('Top K hitters Stats')

        # fig = plt.figure(figsize=(10,10))
        # ax = fig.add_subplot(111)
        # # self.line, = ax.plot(range(10))
        # self.im = ax.imshow(-np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn,  interpolation = 'nearest', vmax=0, vmin=-400000)
        #self.bar_rect = plt.bar([1,2,3], [100,200,300], align='center', alpha=0.3, width=0.2, color='maroon')

        # setup canvas and the toolbar
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.show()
        # self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        # self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.canvas.get_tk_widget().grid(row=0,column=1)
        #toolbar = NavigationToolbar2TkAgg(self.canvas, master)
        #toolbar.update()
        self.canvas._tkcanvas.pack(side='top')



        frame.pack()

    def evaluate(self,val):
        print "entered value:", self.srcbin_entry.get() # data from the Entry / Textbox!
        filter_bin = self.srcbin_entry.get()

    def Refresher(self):
        #text.configure(text=time.asctime())

        # cap_obj = self.data_queue.get(block=False)
        cap_obj = self.data_queue.get()
        if  cap_obj[0].size == 0:

            root.after(1000, self.Refresher)
        else:
            # databrick sketch
            num_intensities = cap_obj[0].reshape(128,128)
            self.im.set_array(-num_intensities)

            combined = []
            for idx, src in enumerate(cap_obj[1]):
                combined.append(src + "\n - \n" + cap_obj[2][idx])
            y_pos = np.arange(len(combined))

            # # TODO(abhishek): Push this to below ==0: block (to avoid re-drawing all the time)?


            if self.num_graphed == 0:

                self.bar_rect = plt.bar(y_pos, cap_obj[3], align='center', alpha=0.3, width=0.2, color='maroon')
                self.num_graphed += 1
            else:
                #topkplot = self.fig.add_subplot(gs[2,:])
                #topkplot.set_title('Top K hitters Stats')
                for i in range(len(combined)):
                    for rect, h in zip(self.bar_rect, cap_obj[3]):
                        rect.set_height(h)


            plt.xticks(y_pos, combined)
            plt.ylabel('# of Bytes')
            plt.xlabel('Top %d hitters (src ip - dst ip)' %len(combined))


            # #plt.pause(0.3) # --- > Culprit -- pops up another window!!? Check the top import here comments to avoid pyplot
            # anno3.remove()

            self.canvas.draw()
            root.after(1000, self.Refresher) # eve

class FlowtransmitImpl(ip_proto_capnp.Flowtransmit.Server):
    "Implementation of Flow Transmit Interface in the schema file"

    def src(self, databrick, hitters, _context, **kwargs):
        #addresses = store_data_capnp.AddressBook.new_message(people=databrick)
        #people = addresses.init('people', 128*128)
        # people = addresses.init('people', 128*128)
        # people = databrick
        #logging.info("databrick rx: #of packets:%d"%sum(people))
        #converting to numpy array and send them to queue
        np_databrick = np.array(databrick)
        print np_databrick

        #print np_databrick[0]
        count_zeros = 0
        for d in range(len(np_databrick)):
            if np_databrick[d] == 0:
                count_zeros += 1
            # print np_databrick[d]

        logging.info("# of zeros :%d, max: %d, min: %d"%(count_zeros, max(np_databrick), min(np_databrick)))

        src_hitters_li = []
        dst_hitters_li = []
        hitter_bytes = []

        for h in hitters:
            src_hitters_li.append(h.ipsrc)
            dst_hitters_li.append(h.ipdst)
            hitter_bytes.append(h.bytes)

        logging.info("Putting data brick and hitters in the shared process queue")
        # logging.warn("CHECKKK Databrick:: %d"%(databrick))

        data_queue.put((np_databrick, src_hitters_li, dst_hitters_li, hitter_bytes))

        try:
            filter_bin = interactive_filter_queue.get(block = False)
            logging.info("filter bin entered: %d",int(filter_bin))
            return int(filter_bin)
        except:
            logging.info("Nothing was entered")
            return

def listen_conn_process(data_queue, interactive_filter_queue, port_number):
    address = "*:"+ str(port_number)
    server = capnp.TwoPartyServer(address,bootstrap=FlowtransmitImpl())
    custom_config.ConfigLoggerAndFlags()
    logging.info("Listening to Incoming connections on port:%d"%port_number)
    server.run_forever()

# root = Tkinter.Tk()
# app = App(root)
# root.mainloop()

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

    root = tk.Tk()
    app = App(master=root, data_queue=data_queue,interactive_filter_queue=interactive_filter_queue)
    # app = App(r,)
    root.title("AMON Viz")
    #app.Refresher()
    #root.mainloop()
    root.mainloop()