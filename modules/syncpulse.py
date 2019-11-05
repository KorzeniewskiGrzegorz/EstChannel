#! /usr/bin/python
import numpy as np 
import matplotlib.pyplot as plt

def  syncpulse(Fs,duration):

	R = 0.5
	wd = duration - 0.1

	t = np.arange(0,wd*R,1/Fs)
	s1 = 1* np.sin(2*np.pi*5e3*t)
	s2 = 1* np.sin(2*np.pi*20e3*t)


	s = np.append(s1 ,s2)
	ISync = np.append(s ,np.zeros(int(Fs*0.1)+1))
	#plt.plot(ISync)
	#plt.show()
	return ISync


def main():
	
	Fs = 20e6  # sample freq [Hz]
	duration = 0.6 # signal duration [s]



	sync = syncpulse(Fs,duration)


if __name__ == '__main__':
    main()