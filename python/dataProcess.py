#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from offcalc import offcalc



#%%%%%%%%%5%%%%%%%%%%%%%
def dataProcess(Fs , #Sample freq
	R = 0.99, # ratio, the same as in generator script
	calibrationOffsetTime = 1,# calibration time [s] , corresponds to parameters of signal generation
	offman = 0,
	wd = 10,
	path = "/dev/shm/",
	offsetThreshold = 0.003,
	offsetTime = 0.1):
	ruidoR = np.fromfile(path + "ruidoR.dat",'float32')
	ruidoI = np.fromfile(path + "ruidoI.dat",'float32')
	ruidoC = ruidoR + 1j * ruidoI
	del ruidoR,ruidoI

	dataR = np.fromfile(path + "dataR.dat",'float32')
	dataI = np.fromfile(path + "dataI.dat",'float32')
	dataC = dataR + 1j * dataI
	del dataR,dataI

	lenRRaw=len(ruidoC)
	lenDRaw=len(dataC)



	offset = offcalc(dataC.real,Fs,0.003,0.05)

	#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	#Calibration processing


	F = 1/calibrationOffsetTime
	calibrationOffset = calibrationOffsetTime * Fs  #conversion from time to samples




	# signal calibration
	offset =(-1) *(offcalc(dataC.real,Fs,0.003,0.1))-offman  #received samples offset due to hardware & software lag [samples];

	ruidoC = ruidoC[ int(calibrationOffset)    :    int(calibrationOffset*2-(Fs/F)*(1-R)) ];
	#print(ruidoC[int(calibrationOffset)])
	#print(ruidoC[int(calibrationOffset)-1])
	#print(ruidoC[int(calibrationOffset*2-(Fs/F)*(1-R))])
	#print(ruidoC[int(calibrationOffset*2-(Fs/F)*(1-R))-1])

	dataC = dataC[int(calibrationOffset+offset)    :    int(calibrationOffset*2-(Fs/F)*(1-R) +offset)  ];

	#plt.plot(dataC.real)
	#plt.show()

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

	plt.plot(np.abs(Ryx))
	plt.show()


def main():
	Fs = 20e6 #Sample freq
	R = 0.99; # ratio, the same as in generator script
	calibrationOffsetTime = 1# calibration time [s] , corresponds to parameters of signal generation
	offman = 30;
	wd = 10; # window duration [us] for the correlation purpose
	path = "/dev/shm/"

	dataProcess(Fs,R,calibrationOffsetTime,offman,wd,path)


if __name__ == '__main__':
    main()
