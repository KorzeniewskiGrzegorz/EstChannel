#! /usr/bin/python
import sys
import os
if sys.version_info[0] < 3:
	from Tkinter import *
	import tkFileDialog
else:
	from tkinter import *


sys.path.insert(1, '/home/grzechu/git/EstChannel/modules')

import numpy as np 
import tkMessageBox
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.pyplot as plt

from routine_remote import * 
from routine_stat import *

############ GLOBAL ################################################
Fs = 38e6
Fr = 2170e6
Ryx = None
path = "mediciones"
count = 0
shiftedRyx = None
offman = 0
bw = 28e6
wd = 10
mode = "Remote"
####################################################################

class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        #self.text_space.config(state=NORMAL)
        self.text_space.insert("end", string)
        self.text_space.see("end")
        #self.text_space.config(state=DISABLED)

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

def enableFields():

	executebutton.config(state=NORMAL)
	entryFr.config(state=NORMAL)
	entryFs.config(state=NORMAL)
	entryBw.config(state=NORMAL)
	entryWd.config(state=NORMAL)

	savebutton.config(state=NORMAL)
	folderButton.config(state=NORMAL)

def disableFields():
	executebutton.config(state=DISABLED)
	entryFs.config(state=DISABLED) 
	entryFr.config(state=DISABLED) 
	entryBw.config(state=DISABLED) 
	entryWd.config(state=DISABLED)
	savebutton.config(state=DISABLED)
	folderButton.config(state=DISABLED)

def work():
	global Ryx,shiftedRyx
	
	disableFields()
	
	plt.clf()
	plt.title('Estimated impulse response')
	plt.ylabel('Amplitude')
	plt.xlabel('Time [us]')
	fig.canvas.draw()

	if mode == "Remote":
		Ryx = routine_remote(Fs,Fr,bw,wd=wd,offman=offman)
	else :
		Ryx = routine_stat(Fs,Fr,bw,wd=wd,offman=offman)


	if Ryx is not None:
		print "\n"
		print '>'*80 
		print '>'*80 
		shiftedRyx = Shifted(Ryx)
		updatePlot()
		
	else:
		print("Try again")

	enableFields()


def start():
	#global Ryx
	thread = threading.Thread(target=work)
	thread.start()
	#Ryx = np.fromfile(path+'m1.dat','double')
	#work()
	
def searchFileIter(pathDir,fileName):


	number =None
	for i in range(1,1000):
		
		if os.path.isfile(pathDir+"/"+fileName+str(i)+'.dat'):
			pass
		else:
			number =  i
			break
	return str(number) 



def updateEntry():
	global path
	entrySave.delete(0, 'end')
	entrySave.config(state=NORMAL)
	entryFolder.delete(0, 'end')
	entryFolder.config(state=NORMAL)

	entryFolder.insert(END, path)
	folder = entryFolder.get()

	fileName = "Fs{0:g}-Fr{1:g}-bw{2:g}-wd{3:g}--".format(Fs/1e6,Fr/1e6,bw/1e6,wd)
	fileName = fileName.replace(".","_")
	entrySave.insert(END, fileName+searchFileIter(path,fileName)+".dat")


def updatePlot():
	global Ryx

	l = len(Ryx)
	range_b = l/Fs 

	t=np.arange(0,l)*1e6/Fs

	plt.clf()
	plt.stem(t,Ryx)
	plt.title('Estimated impulse response')
	plt.ylabel('Amplitude')
	plt.xlabel('Time [us]')
	fig.canvas.draw()
	
	updateEntry()
	
	enableFields()

def save(p):
	global Ryx

	f = path+"/"+p
	Ryx.tofile(path+"/"+p)
	print ("Impulse response saved in "+f)
	updateEntry()


def updateFolder(p):
	global path
	path =tkFileDialog.askdirectory(initialdir = "/home/udg/git/EstChannel/mediciones")

	if not os.path.isdir(path):
		os.makedirs(path)
	updateEntry()


def updateShift(direction):
	global Ryx,shiftedRyx

	Ryx = shiftedRyx.shift(direction)
	updatePlot()

def left(event):
	updateShift(-1)
	
def right(event):
	updateShift(1)
	

def setBw(p):
	global bw
	bw = float(p*1e6)	

def setFs(p):
	global Fs
	Fs = float(p*1e6)

def setFr(p):
	global Fr
	Fr = float(p*1e6)		

def setWd(p):
	global wd
	wd = float(p)	

def change_dropdown(*args):
    global mode
    mode = tkvar.get()
	

########
root = Tk()
root.title("Channel sounding")
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

varFs =  IntVar(value=int(Fs/1e6))  # initial value

try:
	varFs.trace("w", lambda name, index, mode, var=varFs: setFs(varFs.get()))
except ValueError as err:
	pass

entryFs =  Spinbox(etrFrame, from_=1, to=38, textvariable=varFs )
entryFs.pack(side=TOP)
entryFs.config(state=NORMAL)
############

###### Carrier frequency
labelFr = Label(lblFrame, text="Carrier freq. [MHz]:")
labelFr.pack(side=TOP)

varFr =  IntVar(value=int(Fr/1e6))  # initial value

try:
	varFr.trace("w", lambda name, index, mode, var=varFr: setFr(varFr.get()))
except ValueError as err:
	pass

entryFr =  Spinbox(etrFrame, from_=300, to=3800,increment =10, textvariable=varFr )
entryFr.pack(side=TOP)
entryFr.config(state=NORMAL)
############

 
###### bandwidth
labelBw = Label(lblFrame, text="Bandwidth [MHz]:")
labelBw.pack(side=TOP)


varBw =  DoubleVar(value=bw/1e6)  # initial value

try:
	varBw.trace("w", lambda name, index, mode, var=varBw: setBw(varBw.get()))
except ValueError as err:
	pass

entryBw =  Spinbox(etrFrame, from_=1, to=28,increment = 0.5, textvariable=varBw )
entryBw.pack(side=TOP)
entryBw.config(state=NORMAL)
############

##### wd
labelwd = Label(lblFrame, text="Window duration [us]:")
labelwd.pack(side=TOP)

varWd =  IntVar(value=wd)  # initial value

try:
	varWd.trace("w", lambda name, index, mode, var=varWd: setWd(varWd.get()))
except ValueError as err:
	pass

entryWd = Spinbox(etrFrame, from_=1, to=100000, textvariable=varWd )
entryWd.pack(side=TOP)
entryWd.config(state=NORMAL)
######## 

####### buttons

tkvar = StringVar(root)
choices = { 'Remote','Stationary'}
tkvar.set('Remote') # set the default option
popupMenu = OptionMenu(buttonFrame, tkvar, *choices)
popupMenu.pack()
tkvar.trace('w', change_dropdown)

executebutton = Button(buttonFrame, text="Run", command=start)
executebutton.pack(side = BOTTOM) 

###########

dataframe = Frame(root)
dataframe.pack(side = LEFT)

fig = plt.figure(1)
plt.title('Estimated impulse response')
plt.ylabel('Amplitude')
plt.xlabel('Time [us]')


canvas = tkagg.FigureCanvasTkAgg(fig, master=dataframe)
plot_widget = canvas.get_tk_widget()
plot_widget.pack(side = TOP)
toolbar = tkagg.NavigationToolbar2TkAgg(canvas, dataframe)
toolbar.pack(side = TOP)

######################
saveframe = Frame(dataframe)
saveframe.pack(side = BOTTOM)
lSaveFrame = Frame(saveframe)
lSaveFrame.pack(side = LEFT)
eSaveFrame = Frame(saveframe)
eSaveFrame.pack(side = LEFT)
sSaveFrame = Frame(saveframe)
sSaveFrame.pack(side = LEFT)

labelSave = Label(lSaveFrame, text="File name:")
labelSave.pack(side=TOP)

entryFolder = Entry(eSaveFrame, width=50)
entryFolder.pack(side=TOP)
entryFolder.config(state=DISABLED)

labelSave = Label(lSaveFrame, text="Path to folder:")
labelSave.pack(side=TOP)
entrySave = Entry(eSaveFrame, width=50)
entrySave.pack(side=TOP)
entrySave.config(state=DISABLED)

folderButton = Button(sSaveFrame, text="Update folder", command= lambda: updateFolder(entryFolder.get()))
folderButton.pack(side=TOP) 
folderButton.config(state=DISABLED)

savebutton = Button(sSaveFrame, text="Save", command= lambda: save(entrySave.get()))
savebutton.pack(side=TOP) 
savebutton.config(state=DISABLED)






#######################
root.bind('<Left>', left)
root.bind('<Right>', right)

###########


root.mainloop()
