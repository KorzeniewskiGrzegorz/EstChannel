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
        #self.text_space.see("end")
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
	plt.xlabel('Time [us]')
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
	plt.xlabel('Time [us]')
	fig.canvas.draw()
	
	updateEntry()
	savebutton.config(state=NORMAL)
	rerunbutton.config(state=NORMAL)
	entryRerun.config(state=NORMAL)


def save(p):
	global Ryx
	Ryx.tofile(p)
	print ("Impulse response saved in "+p)
	updateEntry()

def rerun(p):
	global Ryx,shiftedRyx
	print("reruning data processing with offset{}".format(p))

	Ryx = dataProcess(Fs,offman=int(p),offsetTime = 0.5,offsetThreshold = 0.004,plotMode=False)
	shiftedRyx = Shifted(Ryx)
	updatePlot()
	print("Done")
	print '>'*80 
	print '>'*80 


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
root.geometry("1500x800")

mainframe = Frame(root)
mainframe.pack(side = LEFT)


executebutton = Button(mainframe, text="Run", command=start)
executebutton.pack(side = BOTTOM)              


text_box = Text(mainframe)
text_box.pack()
sys.stdout = StdRedirector(text_box)

###########

dataframe = Frame(root)
dataframe.pack(side = LEFT)

fig = plt.figure(1)
#plt.ion()
plt.ylabel('Amplitude')
plt.xlabel('Time [us]')


canvas = FigureCanvasTkAgg(fig, master=dataframe)
plot_widget = canvas.get_tk_widget()
plot_widget.pack(side = TOP)

######################
saveframe = Frame(dataframe)
saveframe.pack(side = BOTTOM)

labelSave = Label(saveframe, text="Path to file:")
labelSave.pack(side=LEFT)
entrySave = Entry(saveframe, width=50)
entrySave.pack(side=LEFT)
entrySave.config(state=DISABLED)

savebutton = Button(saveframe, text="Save", command= lambda: save(entrySave.get()))
savebutton.pack(side=RIGHT) 
savebutton.config(state=DISABLED)

######################
rerunframe = Frame(dataframe)
rerunframe.pack(side = BOTTOM)

labelRerun = Label(rerunframe, text="Manual offset:")
labelRerun.pack(side=LEFT)
entryRerun = Entry(rerunframe, width=50)
entryRerun.pack(side=LEFT)
entryRerun.config(state=DISABLED)

rerunbutton = Button(rerunframe, text="Rerun with offset", command= lambda: rerun(entryRerun.get()))
rerunbutton.pack(side=RIGHT)
rerunbutton.config(state=DISABLED)

#######################
root.bind('<Left>', left)
root.bind('<Right>', right)

###########


root.mainloop()
