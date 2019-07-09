import sys
import numpy as np 
import matplotlib.pyplot as plt

def whiteNoiseGen(Fs,R =0.99,segundos = 1,path ='/dev/shm/'):

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
