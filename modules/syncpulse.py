#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt

def  syncpulse(Fs,duration):

	R = 0.5
	wd = duration - 0.1

	ISync = np.zeros(int(Fs*wd))

	ISync[int(Fs*wd*(1-R)):] = 5

	ISync = np.append (ISync, np.zeros(int(Fs*0.1)+1))

	return ISync


def main():
	
	Fs = 20e6  # sample freq [Hz]
	duration = 0.6 # signal duration [s]



	sync = syncpulse(Fs,duration,)


if __name__ == '__main__':
    main()