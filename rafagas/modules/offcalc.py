#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def offcalc(data,Fs):
	
	sync = np.abs(data)


	signal = sync[int((0.1+0.02)*Fs) : int((0.1+0.04)*Fs)]

	noise  = sync[int((0.1-0.04)*Fs) : int((0.1-0.02)*Fs)]


	meanSignal = np.mean(signal)
	meanNoise  = np.mean(noise)

	ratio = meanSignal / meanNoise

	threshold = meanNoise +0.2*ratio*meanNoise;
	offset = int(np.argwhere(sync > threshold)[0] +0.1*Fs ) -30;

	return offset



