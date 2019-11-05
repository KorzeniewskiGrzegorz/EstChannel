#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from offcalc import offcalc
from SNRcalc import SNRcalc
from xCorrelation import xCorrelation
import time

#%%%%%%%%%5%%%%%%%%%%%%%
def dataProcess(Fs , #Sample freq
	wd = 100,
	path = "/dev/shm/",
	offman = 0,
	plotMode=False):
	ruidoR = np.fromfile(path + "ruidoR.dat",'float32')
	ruidoI = np.fromfile(path + "ruidoI.dat",'float32')


	if len(ruidoR) != len(ruidoI):
		print '!'*40
		print "WARNING! SIZE ERROR OF TX SAMPLES"
		print "I:{}".format(len(ruidoR))
		print "Q:{}".format(len(ruidoI))
		print '!'*40
	
	ruidoC = ruidoR + 1j * ruidoI


	del ruidoR,ruidoI

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

	ruidoC = ruidoC[ int(calibrationOffset) : int(calibrationOffset*Fs) ];
	dataC  = dataC [ offset : int(offset+Fs)  ];

	start=time.time()

	Ryx = xCorrelation(ruidoC,dataC,Fs,wd)

	end = time.time()
	print end-start

	if plotMode :
		plt.stem(np.abs(Ryx))
		plt.show()
	else:
		return Ryx


def main():
	Fs = 38e6 #Sample freq
	wd = 10; # window duration [us] for the correlation purpose
	path = "/dev/shm/"
	
	dataProcess(Fs,wd,path,plotMode = True)


if __name__ == '__main__':
    main()
