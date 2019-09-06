#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from offcalc import offcalc



#%%%%%%%%%5%%%%%%%%%%%%%
def dataProcess(Fs , #Sample freq
	wd = 100,
	path = "/dev/shm/",
	offman = 0,
	plotMode=False):
	ruidoR = np.fromfile(path + "ruidoR.dat",'float32')
	ruidoI = np.fromfile(path + "ruidoI.dat",'float32')
	ruidoC = ruidoR + 1j * ruidoI
	del ruidoR,ruidoI

	dataR = np.fromfile(path + "dataR.dat",'float32')
	dataI = np.fromfile(path + "dataI.dat",'float32')
	dataC = dataR + 1j * dataI
	del dataR,dataI

	#lenRRaw=len(ruidoC)
	#lenDRaw=len(dataC)





	#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	#Calibration processing

	calibrationOffset = 0.2 *Fs  #conversion from time to samples

	# signal calibration
	offset = offcalc(dataC,Fs) + offman #received samples offset due to hardware & software lag [samples];


	dataR = np.fromfile(path + "fdataR.dat",'float32')
	dataI = np.fromfile(path + "fdataI.dat",'float32')

	dataC = dataR + 1j * dataI
	del dataR,dataI

	ruidoC = ruidoC[ int(calibrationOffset) : int(calibrationOffset*Fs) ];
	dataC  = dataC [ offset : int(offset+Fs)  ];


	lenR=len(ruidoC)
	lenD=len(dataC)


	#TODO
	#calibrated data plotting


	N=int( wd*Fs/1000000) # conversion of window duration from miliseconds to samples

	v=int(np.floor(lenD/N)) # number of pulses recorded
	PA = np.zeros((v,N)) + 1j * np.zeros((v,N))


	for i in range(0,v):# Run cross correlation for v times
	    
		x=ruidoC[int(i*N) : int(i*N+N)] #TX
		y=dataC[int(i*N)  : int(i*N+N)] # RX
		
		rxy=np.correlate( x, np.conj(y) , 'full' ) # Cross correlation of the TX and RX conjugated data
		Ryx=np.flip(rxy[0:N],0) # Flip the correlation result and take the first N samples (Ryx(t) = Rxy(-t)
		PA[i] = Ryx

	Ryx = PA.mean(axis=0)
	Ryx = np.abs(Ryx)

	if plotMode :
		plt.plot(np.abs(Ryx))
		plt.show()
	else:
		return Ryx


def main():
	Fs = 20e6 #Sample freq
	wd = 100; # window duration [us] for the correlation purpose
	path = "/dev/shm/"

	dataProcess(Fs,wd,path)


if __name__ == '__main__':
    main()
