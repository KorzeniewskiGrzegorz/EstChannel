#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt

def  syncpulse(Fs,R,duration,wd):

	ISync = np.zeros(int(Fs*duration))


	v = int(duration/wd)
	N = int(Fs*wd) 


	w = np.zeros(int(Fs*wd))
	w[0:int(Fs*wd- Fs*wd*(1-R))] = 5

	i = 1
	ISync[i*N:(i+1)*N] = w 

	return ISync


def main():
	
	Fs = 20e6  # sample freq [Hz]
	R = 0.5 # pulse ratio (0-1 range) for signal break
	duration = 0.2 # signal duration [s]
	wd = 0.1


	sync = syncpulse(Fs,R,duration,wd)


if __name__ == '__main__':
    main()