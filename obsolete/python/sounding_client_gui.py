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
offman = 30
bw = 1.5e6
wd = 10
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
	rerunbutton.config(state=DISABLED)
	entryOffman.config(state=DISABLED)
	entryFs.config(state=DISABLED) 
	entryBw.config(state=DISABLED) 
	plt.clf()
	plt.ylabel('Amplitude')
	plt.xlabel('Time [us]')
	fig.canvas.draw()

	Ryx = sounding_client(Fs,bw,wd=wd,offman=offman)
	if Ryx is not None:
		print "\n"*5
		print '>'*80 
		print '>'*80 
		shiftedRyx = Shifted(Ryx)
		updatePlot()
		
	else:
		print("Try again")

	executebutton.config(state=NORMAL)
	rerunbutton.config(state=NORMAL)
	entryOffman.config(state=NORMAL) 

def rerun():
	global Ryx,shiftedRyx,offman

	executebutton.config(state=DISABLED)
	rerunbutton.config(state=DISABLED)
	entryOffman.config(state=DISABLED)
	entryFs.config(state=DISABLED) 
	entryBw.config(state=DISABLED) 
	print("reruning data processing with offset {}".format(offman))
	print("please wait...")

	Ryx = dataProcess(Fs,wd=wd,offman=offman,offsetTime = 0.5,offsetThreshold = 0.004,plotMode=False)
	shiftedRyx = Shifted(Ryx)
	updatePlot()
	print("Done")
	print '>'*80 
	print '>'*80 

	executebutton.config(state=NORMAL)
	rerunbutton.config(state=NORMAL)
	entryOffman.config(state=NORMAL)
	entryFs.config(state=NORMAL)
	entryBw.config(state=NORMAL)




def start():
	#global Ryx
	thread = threading.Thread(target=work)
	thread.start()
	#Ryx = np.fromfile(path+'m1.dat','double')
	#work()
	
def rr():

	thread = threading.Thread(target=rerun)
	thread.start()


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

	l = len(Ryx)
	
	range_b = int(wd*1e-6)
	t=np.arange(0,range_b,1/Fs)*1e6/Fs
	plt.clf()
	plt.plot(Ryx)
	plt.ylabel('Amplitude')
	plt.xlabel('Time [us]')
	fig.canvas.draw()
	
	updateEntry()
	savebutton.config(state=NORMAL)
	rerunbutton.config(state=NORMAL)
	entryOffman.config(state=NORMAL)
	entryFs.config(state=NORMAL)
	entryBw.config(state=NORMAL)

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
	
def setOffman(p):
	global offman
	offman = int(p)	

def setBw(p):
	global bw
	bw = float(p*1e6)	

def setFs(p):
	global Fs
	Fs = float(p*1e6)	

def setWd(p):
	global wd
	wd = float(p)	
	

########
root = Tk()
root.title("Sounding Client")
root.protocol('WM_DELETE_WINDOW', _destroyWindow)
root.geometry("1350x600")


mainframe = Frame(root)
mainframe.pack(side = LEFT, padx =20, pady = 20)


######################

text_box = Text(mainframe)
text_box.pack()
sys.stdout = StdRedirector(text_box)

actionFrame = Frame(mainframe)
actionFrame.pack(side = BOTTOM)

paramFrame = Frame(actionFrame)
paramFrame.pack(side = LEFT, padx =20, pady = 20)

buttonFrame = Frame(actionFrame)
buttonFrame.pack(side = LEFT, padx =20, pady = 20)

lblFrame = Frame(paramFrame)
lblFrame.pack(side = LEFT)

etrFrame = Frame(paramFrame)
etrFrame.pack(side = RIGHT)


###### Sampling frequency
labelFs = Label(lblFrame, text="Sampling freq. [MHz]:")
labelFs.pack(side=TOP)

varFs =  IntVar(value=20)  # initial value

try:
	varFs.trace("w", lambda name, index, mode, var=varFs: setFs(varFs.get()))
except ValueError as err:
	pass

entryFs =  Spinbox(etrFrame, from_=1, to=20, textvariable=varFs )
entryFs.pack(side=TOP)
entryFs.config(state=NORMAL)
############

 
###### bandwidth
labelBw = Label(lblFrame, text="Bandwidth [MHz]:")
labelBw.pack(side=TOP)


varBw =  DoubleVar(value=20)  # initial value

try:
	varBw.trace("w", lambda name, index, mode, var=varBw: setBw(varBw.get()))
except ValueError as err:
	pass

entryBw =  Spinbox(etrFrame, from_=1, to=20, textvariable=varBw )
entryBw.pack(side=TOP)
entryBw.config(state=NORMAL)
############

##### offset
labelOffset = Label(lblFrame, text="Manual offset [samples]:")
labelOffset.pack(side=TOP)

varOff =  IntVar(value=offman)  # initial value

try:
	varOff.trace("w", lambda name, index, mode, var=varOff: setOffman(varOff.get()))
except ValueError as err:
	pass

entryOffman = Spinbox(etrFrame, from_=-100, to=100, textvariable=varOff )
entryOffman.pack(side=TOP)
entryOffman.config(state=NORMAL)
######## 

##### wd
labelwd = Label(lblFrame, text="Window duration [us]:")
labelwd.pack(side=TOP)

varWd =  IntVar(value=10)  # initial value

try:
	varWd.trace("w", lambda name, index, mode, var=varWd: setWd(varWd.get()))
except ValueError as err:
	pass

entryWd = Spinbox(etrFrame, from_=1, to=100000, textvariable=varWd )
entryWd.pack(side=TOP)
entryWd.config(state=NORMAL)
######## 

####### buttons
rerunbutton = Button(buttonFrame, text="Rerun data process", command= rr)
rerunbutton.pack(side=BOTTOM)
rerunbutton.config(state=DISABLED)  

executebutton = Button(buttonFrame, text="Run", command=start)
executebutton.pack(side = BOTTOM) 

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




#######################
root.bind('<Left>', left)
root.bind('<Right>', right)

###########


root.mainloop()
