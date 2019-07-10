#! /usr/bin/python
import sys
import os
if sys.version_info[0] < 3:
    from Tkinter import *
else:
	from tkinter import *

import numpy as np 
import tkMessageBox
from sounding_client import * 

class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=NORMAL)
        self.text_space.insert("end", string)
        self.text_space.see("end")
        self.text_space.config(state=DISABLED)



Fs = 20e6
Ryx = None

def _destroyWindow():
    root.quit()
    root.destroy()


def work():
	executebutton.config(state=DISABLED)

	Ryx = sounding_client(Fs)
	if Ryx is not None:
		print(Ryx)
	else:
		print("Try again")

	executebutton.config(state=NORMAL)

	#update of the plot i chuj
def start():

	thread = threading.Thread(target=work)
	thread.start()

	



	

########
w, h = 300, 200
root = Tk()
root.title("siema")
root.protocol('WM_DELETE_WINDOW', _destroyWindow)
root.geometry("1000x500")

mainframe = Frame(root)
mainframe.grid(column=0, row=0)


executebutton = Button(mainframe, text="Run", command=start)
executebutton.grid(column=0, row=5)              


text_box = Text(mainframe)
text_box.grid(column=1, row=5)
sys.stdout = StdRedirector(text_box)

#####


root.mainloop()
