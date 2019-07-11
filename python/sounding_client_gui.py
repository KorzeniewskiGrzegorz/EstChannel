#! /usr/bin/python
import sys
import os
if sys.version_info[0] < 3:
    from Tkinter import *
else:
	from tkinter import *

import numpy as np 
import tkMessageBox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from sounding_client import * 

############ GLOBAL ################################################
Fs = 20e6
Ryx = None
path = "mediciones/"
count = 0
shiftedRyx = None
####################################################################

class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=NORMAL)
        self.text_space.insert("end", string)
        self.text_space.see("end")
        self.text_space.config(state=DISABLED)

class Shifted:
	def __init__(self,org ):
		self.count=0
		if(org is not None):
			self.data = org.copy()
			self.len_data = org.size

	def shift(self,direction):

		self.count += direction
		self.data = np.roll(self.data,direction)
		newData = self.data.copy()
		if self.count < 0:
	   		newData[self.len_data + self.count  :  self.len_data ] = np.zeros((-1)*self.count)

	   	return newData

####################################################################

def _destroyWindow():
    root.quit()
    root.destroy()


def work():
	global Ryx,shiftedRyx
	executebutton.config(state=DISABLED)
	plt.clf()
	plt.ylabel('Amplitude')
	plt.xlabel('Time [ns]')
	fig.canvas.draw()

	Ryx = sounding_client(Fs)
	if Ryx is not None:
		print "\n"*5
		print '>'*80 
		print '>'*80 
		shiftedRyx = Shifted(Ryx)
		updatePlot()
		
	else:
		print("Try again")

	executebutton.config(state=NORMAL)


def start():
	#global Ryx
	thread = threading.Thread(target=work)
	thread.start()
	#Ryx = np.fromfile(path+'m1.dat','double')
	#work()
	
def searchFileIter(pathDir):
	number =None
	for i in range(1,1000):
		
		if os.path.isfile(pathDir+'m'+str(i)+'.dat'):
			pass
		else:
			number =  i
			break
	return str(number) 



def updateEntry():
	entrySave.delete(0, 'end')
	entrySave.config(state=NORMAL)
	entrySave.insert(END,path + "m"+searchFileIter(path)+".dat")


def updatePlot():
	global Ryx

	range_a= int(0*Fs)
	range_b = int(10e-6*Fs)
	t=np.arange(range_a,range_b) / Fs *1e6
	plt.clf()
	plt.plot(t,Ryx)
	plt.ylabel('Amplitude')
	plt.xlabel('Time [ns]')
	fig.canvas.draw()
	
	updateEntry()
	savebutton.config(state=NORMAL)
	


def save(p):
	global Ryx
	Ryx.tofile(p)
	print ("Impulse response saved in "+p)
	updateEntry()




def updateShift(direction):
	global Ryx,shiftedRyx

	Ryx = shiftedRyx.shift(direction)
	updatePlot()

def left(event):
	updateShift(-1)
	
def right(event):
	updateShift(1)
	
	


	

########
w, h = 300, 200
root = Tk()
root.title("siema")
root.protocol('WM_DELETE_WINDOW', _destroyWindow)
root.geometry("1430x500")

mainframe = Frame(root)
mainframe.grid(column=0, row=0)


executebutton = Button(mainframe, text="Run", command=start)
executebutton.grid(column=0, row=5)              


text_box = Text(mainframe)
text_box.grid(column=1, row=5)
sys.stdout = StdRedirector(text_box)

###########

fig = plt.figure(1)
#plt.ion()
plt.ylabel('Amplitude')
plt.xlabel('Time [us]')


canvas = FigureCanvasTkAgg(fig, master=root)
plot_widget = canvas.get_tk_widget()
plot_widget.grid(row=0, column=2)



entrySave = Entry(root, width=50)
entrySave.grid(row=15, column=2)
entrySave.config(state=DISABLED)

savebutton = Button(mainframe, text="Save", command= lambda: save(entrySave.get()))
savebutton.grid(column=2, row=30)  
savebutton.config(state=DISABLED)


root.bind('<Left>', left)
root.bind('<Right>', right)

###########


root.mainloop()
