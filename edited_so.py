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

from Tkinter import Label, Entry

class Application(tk.Frame):
# class Application:
    def __init__(self, master=None, shared_queue=None, interactive_filter_queue=None):
        self.frame = tk.Frame.__init__(self,master)
        # self.frame = tk.Frame(master)
        self.toolbar = NavigationToolbar2TkAgg(self.frame, master)
        self.data_queue = shared_queue
        self.interactive_queue = interactive_filter_queue
        self.createWidgets()


    def createWidgets(self):
        self.fig = plt.figure(figsize=(10,10))
        # ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        self.gs = GridSpec(4,1)
        ax = self.fig.add_subplot(self.gs[0:2,:])
        self.im = ax.imshow(-np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest', vmax=0, vmin=-400000)


        # bar graph visualization
        self.num_graphed = 0
        self.topkplot = self.fig.add_subplot(self.gs[2,:])
        self.topkplot.set_title('Top K hitters Stats')

        self.canvas = FigureCanvasTkAgg(self.fig,master=root)
        self.canvas.get_tk_widget().grid(row=0,column=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, root)
        # self.toolbar.update()
        # self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.get_tk_widget().grid(row=0,column=1)
        plt.tight_layout()
        # self.plotbutton=tk.Button(master=root, text="plot", command=lambda: self.plot(canvas,ax,im))
        # self.plotbutton = tk.Button(master=self.frame, text="plot", command=lambda: self.plot())
        #self.plotbutton.grid(row=3,column=0)

        self.srcbin_label = Label(master=self.frame, text="Enter the dst bin to filter: ")
        self.srcbin_label.grid(row=3, column=1)
        # self.srcbin_label.pack(side="left")
        self.srcbin_entry = Entry(master=self.frame)
        self.srcbin_entry.grid(row=1, column=0)
        # self.srcbin_entry.pack(side="right")
        self.srcbin_entry.bind("<Return>",self.evaluate)
        self.canvas.show()
        logging.info("Window configured!")
        #return im

    def evaluate(self,val):
        print "entered value:", self.srcbin_entry.get() # data from the Entry / Textbox!
        filter_bin = self.srcbin_entry.get()
        self.interactive_queue.put(filter_bin)



    #def plot(self,canvas,ax,im):
    # TODO(abhishek): change this method to pause/play!
    def plot(self):
        pass
        # self.im.set_array(np.random.random([128,128]))
        # bar_rect = plt.bar([5,0,19], [600,100,200], align='center', alpha=0.3, width=0.2, color='maroon')
        # im = ax.imshow(np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest')
        # self.canvas.draw()




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
            root.after(1000, self.Refresher) # every second...


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
        # filter = filter or 0
        # print "mod filter:",filter
        # return filter
        #return 1
        #print "filter rx:",filter
        #return filter
        #return int(filter)
        #return 5
        #return filter


def listen_conn_process(data_queue, interactive_filter_queue, port_number):
    address = "*:"+ str(port_number)
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

    root = tk.Tk()
    app = Application(master=root, shared_queue=data_queue,interactive_filter_queue=interactive_filter_queue)
    root.title("AMON Viz")
    app.Refresher()
    app.mainloop()
    # logging.info("Control never comes here")
    # cap_conn_process.join()



    # mp_plot_process(data_queue, interactive_filter_queue)
    # cap_conn_process.join()
