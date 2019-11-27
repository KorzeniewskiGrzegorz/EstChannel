#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from numpy import argmax, sqrt, mean, absolute, linspace, log10, logical_and, average, diff, correlate,argwhere,flip
from matplotlib.mlab import find


def SNRcalc(data,Fs,offId):

	data = np.real(data) + np.imag(data)

	signal = data[ int(offId -0.16*Fs):int(offId -0.14*Fs)]

	noise = data[int(offId -0.06*Fs): int(offId -0.04*Fs)]

	avgSigPwr = np.mean(np.square(signal))
	avgNsPwr = np.mean(np.square(noise))

	snr = 10*np.log10(avgSigPwr/avgNsPwr)

	return snr


