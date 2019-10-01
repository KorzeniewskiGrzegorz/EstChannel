#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from numpy import argmax, sqrt, mean, absolute, linspace, log10, logical_and, average, diff, correlate,argwhere,flip
from matplotlib.mlab import find


def offcalc(data,Fs):

	sig = np.real(data) + np.imag(data)

	zx = np.where(np.diff(np.sign(sig)))[0]  

	der = diff(zx)

	flips= flip(der,0)


	threshold = max(flips[1:int(len(flips)/10)]) * 5 
	idOdwrocone = argwhere(flips > threshold)[0]
	idx = len(zx) - idOdwrocone
	offset = int(zx[idx] + der[idx]+ 0.1*Fs);

	return offset




