import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
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

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.createWidgets()

    def createWidgets(self):
        fig=plt.figure(figsize=(8,8))
        # ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        gs=GridSpec(3,1)
        ax = fig.add_subplot(gs[0:2,:])
        im = ax.imshow(np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest')
        topkplot = fig.add_subplot(gs[2,:])
        bar_rect = plt.bar([1,2,3], [100,200,300], align='center', alpha=0.3, width=0.2, color='maroon')
        canvas=FigureCanvasTkAgg(fig,master=root)
        canvas.get_tk_widget().grid(row=0,column=1)
        canvas.show()

        self.plotbutton=tk.Button(master=root, text="plot", command=lambda: self.plot(canvas,ax,im))
        self.plotbutton.grid(row=0,column=0)

        logging.info("Window configured!")




    def plot(self,canvas,ax,im):
        im.set_array(np.random.random([128,128]))
        bar_rect = plt.bar([5,0,19], [600,100,200], align='center', alpha=0.3, width=0.2, color='maroon')
        # im = ax.imshow(np.random.random([128,128]), origin = 'upper', cmap=plt.cm.RdYlGn, interpolation = 'nearest')
        canvas.draw()
        # ax.clear()
        # for line in sys.stdout: #infinite loop, reads data of a subprocess
        #     theta=line[1]
        #     r=line[2]
        #     ax.plot(theta,r,linestyle="None",maker='o')
        #     canvas.draw()
        #     ax.clear()
        #     #here set axes



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

        print np_databrick[0]
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

        #data_queue.put((np_databrick, src_hitters_li, dst_hitters_li, hitter_bytes))
        # filter = interactive_filter_queue.get()
        # print "raw filter:",filter
        # filter = filter or 0
        # print "mod filter:",filter
        # return filter
        return 1
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

    interactive_filter_queue = manager.Queue()

    cap_conn_process = Process(target=listen_conn_process, args=(data_queue,interactive_filter_queue, port_number))
    cap_conn_process.start()
    logging.info("Cap'n Proto process started on port:%d"%port_number)

    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

    # mp_plot_process(data_queue, interactive_filter_queue)
    # cap_conn_process.join()
