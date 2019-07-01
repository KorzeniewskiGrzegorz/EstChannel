#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def offcalc(signal,Fs,threshold,r,calibrationTime):
	
	data = signal[int((calibrationTime-r)*Fs):int((calibrationTime+r)*Fs)]

	a = []
	for i in range(0,len(data)):
		if data[i] < threshold:
			a.append(i +(calibrationTime-r)*Fs)     
	   

	#plt.plot(a)
	#plt.show()


	v=int(np.floor(len(a)/1000));
	der=np.diff(a);


	#plt.plot(der)
	#plt.show()

	for i in range(0,v):
		count = 0
		for j in range(0,980):
			if der[int(i*1000+j)]== der[int(i*1000+j+1)]:
				count +=1
	        
			if count > 950:
				start = i*1000 
	               

	pId,prop = find_peaks( der[int(start):int(start+2000)], height=2);


	peak_id = pId[0]
	peak_heigth = prop.values()[0][0]

	#plt.plot(der[int(start):int(start+2000)])
	#plt.show()

	offset = Fs- a[int(start + peak_id - peak_heigth)]
	return offset

