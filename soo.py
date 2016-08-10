import matplotlib, numpy, sys
matplotlib.use('TkAgg')
# matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()

f = Figure(figsize=(12,12), dpi=100)
ax = f.add_subplot(111)

data = (20, 35, 30, 35, 27)

ind = numpy.arange(5)  # the x locations for the groups
width = .5

# rects1 = ax.bar(ind, data, width)
im = ax.imshow(-np.random.random([128,128]), origin = 'upper',   interpolation = 'nearest', vmax=0, vmin=-400000)

fig = plt.figure(figsize=(5,4))
ax2 = fig.add_subplot(111)
im = ax2.imshow(-np.random.random([90,120]), origin = 'upper',   interpolation = 'nearest', vmax=0, vmin=-400000)
fig.show()

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

Tk.mainloop()