#! /usr/bin/python
import sys
import os
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import numpy as np 
import tkMessageBox
from sounding_client import * 


Fs = 20e6


def _destroyWindow():
    app.quit()
    app.destroy()


def start():

	 sounding_client(Fs,plotMode=False)



########
w, h = 300, 200
app = tk.Tk()
app.title("siema")
app.protocol('WM_DELETE_WINDOW', _destroyWindow)
app.geometry("500x500")


#####





B =tk.Button(app,text="Start",command=start)

B.pack()
C =tk.Button(app,text="Stsart",command=start)

C.pack()

app.mainloop()
