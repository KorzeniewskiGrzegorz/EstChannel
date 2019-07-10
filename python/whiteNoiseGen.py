#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt


def whiteNoiseGen(Fs,R =0.99,segundos = 1,path ='/dev/shm/'):
	print("whiteNoiseGen - Generating ...")
	pulseLen = int(Fs*segundos)
	IPulse = np.zeros(int(Fs*segundos))

	IPulse[0:int(Fs*segundos- Fs*segundos*(1-R))] = np.random.randn(1,int(Fs*segundos - Fs*segundos*(1-R)))


	QPulse = np.zeros(int(Fs*segundos))

	#t=np.linspace(0, segundos, num=pulseLen)

	#plt.plot(t,IPulse,'b',t,QPulse,'r')
	#plt.show()



	IPulse.astype('float32').tofile(path + 'IPulse.dat')
	QPulse.astype('float32').tofile(path + 'QPulse.dat')
	print("whiteNoiseGen - Done")
	print("Created files to path "+path)

def main():
	
	Fs = 20e6  # sample freq [Hz]
	R = 0.99 # pulse ratio (0-1 range) for signal break
	segundos = 1 # signal duration [s]
	path="/dev/shm/"

	whiteNoiseGen(Fs)

if __name__ == '__main__':
    main()
