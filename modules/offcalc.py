#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def offcalc(data,Fs):
	
	ot = 0.15

	sync = np.real(data) + np.imag(data)


	signal = sync[int((ot+0.12)*Fs) : int((ot+0.14)*Fs)]

	noise  = sync[int(0.05*Fs) : int(0.07*Fs)]


	meanSignal = np.mean(signal)
	meanNoise  = np.mean(noise)
	
	threshold = meanSignal 


	if meanSignal > meanNoise :
	
		offset = int(np.argwhere(sync[int(0.05*Fs):] > threshold)[0]) + int(0.4*Fs)  -30

	else:

		offset = int(np.argwhere(sync[int(0.05*Fs):] <threshold)[0]) + int(0.4*Fs)  -30


	return offset



