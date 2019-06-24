#! /usr/bin/python
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import numpy as np 


import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from scipy.ndimage.interpolation import shift

Fs = 20e6
range_a= int(0*Fs)
range_b = int(10e-6*Fs)

data = np.fromfile('Ryx.dat','double')
len_data = data.size
t=np.arange(range_a,range_b) / Fs *1e6

def _destroyWindow():
    app.quit()
    app.destroy()


########
w, h = 300, 200
app = tk.Tk()
app.title("siema")
app.protocol('WM_DELETE_WINDOW', _destroyWindow)


#####
fig = plt.figure(1)
#plt.ion()
plt.plot(t,data[range_a:range_b])

canvas = FigureCanvasTkAgg(fig, master=app)
plot_widget = canvas.get_tk_widget()

count = 0
newData = data.copy()

def update(direction):
	global data, count,newData
	count = count + direction
	data = np.roll(data,direction)
   	#y = shift(y, 1, cval=0)
   	newData = data.copy()
   	if count < 0:
   		newData[len_data + count:len_data] = np.zeros((-1)*count) 
	
	plt.clf()
	plt.plot(t,newData)
	fig.canvas.draw()

def left(event):
	update(-1)
	
def right(event):
	update(1)
	

plot_widget.grid(row=0, column=0)
app.bind('<Left>', left)
app.bind('<Right>', right)

def saveRyx():
	newData.tofile('shiftedRyx.dat')

tk.Button(app,text="Save",command=saveRyx).grid(row=1, column=0)

app.mainloop()
