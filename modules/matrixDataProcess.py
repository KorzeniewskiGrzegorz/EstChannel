#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from offcalc import offcalc
from SNRcalc import SNRcalc


#%%%%%%%%%5%%%%%%%%%%%%%
def matrixDataProcess(Fs , #Sample freq
	wd = 100,
	path = "/dev/shm/",
	offman = 0,
	plotMode=False):

	dataR = np.fromfile(path + "fdataR.dat",'float32')
	dataI = np.fromfile(path + "fdataI.dat",'float32')


	if len(dataR) != len(dataI):
		print '!'*40
		print "WARNING! SIZE ERROR OF RX SAMPLES"
		print "I:{}".format(len(dataR))
		print "Q:{}".format(len(dataI))
		print '!'*40
	
	dataC = dataR[0:int(2*Fs)] + 1j * dataI[0:int(2*Fs)]
	del dataR,dataI

	#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	#Calibration processing

	calibrationOffset = 0.6 *Fs  #conversion from time to samples

	# signal calibration
	offset = offcalc(dataC[0:int(Fs*0.6)],Fs) + offman #received samples offset due to hardware & software lag [samples];
	snr = SNRcalc(dataC[0:int(Fs*0.8)],Fs,offset)

	print "SNR: {}".format(snr)

	dataC  = dataC [ offset : int(offset+Fs)  ]

	lenD=len(dataC)


	if 1 ==1 :
		N=int( wd*Fs/1000000) # conversion of window duration from miliseconds to samples

		v=int(np.floor(lenD/N)) # number of pulses recorded
		PA = np.zeros((N,v)) + 1j * np.zeros((N,v))
		

		for i in range(0,v):# Run cross correlation for v times
		    
			y=np.matrix((dataC[int(i*N)  : int(i*N+N)]))# RX
			y = y.transpose();

			ryy= y.dot(y.getH())# Cross correlation of the TX and RX conjugated data
			Ryy= ryy[:,1];

 			PA[:,[i]]=Ryy #Store the results in an array

		ERyy = PA.mean(axis=1) # Average the values 

		
		h= np.abs(ERyy)

	else:
		h = 0

	if plotMode :
		plt.stem(h)
		plt.show()
	else:
		return h


def main():
	Fs = 38e6 #Sample freq
	wd = 10; # window duration [us] for the correlation purpose
	path = "/dev/shm/"

	matrixDataProcess(Fs,wd,path,plotMode = True)


if __name__ == '__main__':
    main()
