#! /usr/bin/python
import sys
import numpy as np 
import matplotlib.pyplot as plt
from syncpulse import *


def whiteNoiseGen(Fs,R =0.01,duration = 1,wd =0.0001, path ='/dev/shm/'):

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

	IData = np.append (ISync, IData)

	data_len =np.size(IData)


	QData = np.zeros(data_len)

	#t=np.linspace(0, duration+syncPulseLen, num=data_len)

	#plt.plot(t,IData,'b',t,QData,'r')
	#plt.show()



	IData.astype('float32').tofile(path + 'IPulse.dat')
	QData.astype('float32').tofile(path + 'QPulse.dat')
	print("whiteNoiseGen - Done")
	print("Created files to path "+path)

def main():
	
	Fs = 20e6  # sample freq [Hz]
	R = 0.01 # pulse ratio (0-1 range) for signal break
	duration = 1 # signal duration [s]
	wd = 0.0001
	path="/dev/shm/"

	whiteNoiseGen(Fs,R)

if __name__ == '__main__':
    main()




#IData = zeros(1,floor(Fs*duration));

#v = segundos/wd;
#N= Fs*wd ;

#for i=1: v
    #w = zeros(1,floor(Fs*wd));
    #w(1,1:floor(Fs*wd)- floor(Fs*wd)*(1-R)) = randn(1,floor(Fs*wd)- floor(Fs*wd)*(1-R));

    #IData(1,(i-1)*N+1:i*N) = w; 
#end


#ISync = syncpulse(Fs,0.5,0.2,0.1);

#IData = [ISync, IData];

#data_len =length(IData);

#%QData = [zeros(1,Fs/4) IData]; % 90 degree delay, quadrature signal
#%QData = QData(1,1:data_len);

#QData = zeros(1,data_len);


#t = 0:1/Fs:(data_len-1)/Fs;

#plot(t,IData,'b',t,QData,'r')

#f = fopen (path+"IPulse.dat", 'wb');
#fwrite (f, IData,'float');
#fclose (f);

#f = fopen (path+"QPulse.dat", 'wb');
#fwrite (f, QData,'float');
#fclose (f);

