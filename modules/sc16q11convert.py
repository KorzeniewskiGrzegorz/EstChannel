#! /usr/bin/python
import numpy as np 
import matplotlib.pyplot as plt

def mult(sig):

	c = np.round(sig*2048)
	c[np.where( c >  2047 )] =  2047
	c[np.where( c < -2048 )] = -2048
	return c

def sc16q11convert(signal):

	i =np.real(signal)
	q =np.imag(signal)
	
	c_i=mult(i)
	c_q=mult(q)

	assert(len(c_i) == len(c_q))
	sig_len = 2 * len(c_i)

	sc = np.zeros(sig_len)
	sc[0:sig_len-1:2] = c_i
	sc[1:sig_len  :2] = c_q

	return sc

def main():
	Fs =38e6
	t = np.arange(0,0.01,1/Fs)
	s_i = 1* np.sin(2*np.pi*5e3*t)
	s_i = s_i / np.amax(s_i)
	s_q = np.zeros(np.size(s_i))

	s = s_i +1j*s_q


	converted = sc16q11convert(s)
	converted.astype('int16').tofile("/dev/shm/" + 'converted.bin')

if __name__ == '__main__':
    main()