#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from syncpulse import *
from sc16q11convert import *


def whiteNoiseGen(Fs,R =0.01,duration = 1,wd =0.0001, path ='/dev/shm/', plotMode =0):

	print("whiteNoiseGen - Generating ...")
	
	IData = np.zeros(int(Fs*duration))

	v = int(duration/wd)
	N = int(Fs*wd)

	for i in range(v): 

		w = np.zeros(int(Fs*wd))
		w[0:int(Fs*wd- Fs*wd*(1-R))] = np.random.randn(1,int(Fs*wd - Fs*wd*(1-R)))
		IData[i*N:(i+1)*N] = w

	syncPulseLen = 0.6 # [s]

	ISync = syncpulse(Fs,syncPulseLen,)

	IData = IData / np.amax(IData) # !!!VERY IMPORTANT!!! necessary to avoid value saturation
	IData = np.append (ISync, IData)

	QData = np.zeros(np.size(IData))

	if plotMode is 1:
		t=np.linspace(0, duration+syncPulseLen, num=data_len)

		plt.plot(t,IData,'b',t,QData,'r')
		plt.show()

	s = IData +1j*QData
	converted = sc16q11convert(s)
	converted.astype('int16').tofile("/dev/shm/" + 'tx.bin')

	IData.astype('float32').tofile(path + 'IPulse.dat')
	QData.astype('float32').tofile(path + 'QPulse.dat')

	IData = np.append (IData, IData)
	IData = IData[0:int(2*Fs)]
	QData = np.zeros(np.size(IData))

	IData.astype('float32').tofile(path + 'ruidoR.dat')
	QData.astype('float32').tofile(path + 'ruidoI.dat')

	print("whiteNoiseGen - Done")
	print("Created files to path "+path)

def main():
	
	Fs = 38e6  # sample freq [Hz]
	R = 0.01 # pulse ratio (0-1 range) for signal break
	duration = 1 # signal duration [s]
	wd = 0.0001
	path="/dev/shm/"

	whiteNoiseGen(Fs,R,plotMode = 0)

if __name__ == '__main__':
    main()

