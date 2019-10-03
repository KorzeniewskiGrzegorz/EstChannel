#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from numba import jit

#@jit
def xCorrelation(ruido,data,Fs,wd):

	lenR=len(ruido)
	lenD=len(data)

	N=int( wd*Fs/1000000) # conversion of window duration from miliseconds to samples

	v=int(np.floor(lenD/N)) # number of pulses recorded
	PA = np.zeros((v,N)) + 1j * np.zeros((v,N))


	for i in range(0,v):# Run cross correlation for v times
	    
		x=ruido[int(i*N) : int(i*N+N)] #TX
		y=data[int(i*N)  : int(i*N+N)] # RX
		
		rxy=np.correlate( x, np.conj(y) , 'full' ) # Cross correlation of the TX and RX conjugated data
		Ryx=np.flip(rxy[0:N],0) # Flip the correlation result and take the first N samples (Ryx(t) = Rxy(-t)
		PA[i] = Ryx

	Ryx = PA.mean(axis=0)
	Ryx = np.abs(Ryx)

	return Ryx


