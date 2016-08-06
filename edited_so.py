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

root=tk.Tk()
app=Application(master=root)
app.mainloop()