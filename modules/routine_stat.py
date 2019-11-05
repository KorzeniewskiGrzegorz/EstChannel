# RX, where the data is generated and processed

import os
import sys
import traceback

import threading
from whiteNoiseGen import whiteNoiseGen
from dataProcess import dataProcess
from matrixDataProcess import matrixDataProcess
from blader_stat import blader_stat
from dcFilter import dcFilter 
from scipy.ndimage.interpolation import shift

def routine_stat(Fs,
			Fr=2400e6,
			bw=1.5e6,
			offman =0,
			plotMode=False,
			path = '/dev/shm/',
			wd = 100,
			):


	print '<'*80 
	print '<'*80 
	print "INIT"
	whiteNoiseGen(Fs)

	######################

	result_available = threading.Event()
	thread = threading.Thread(target=blader_stat, args=(Fs,Fr,bw,result_available,))
	thread.start()
	print("transmitting...")
	result_available.wait()


	dcFilter()


	

	print("processing data ...")

	
	try:
		Ryx = matrixDataProcess(Fs,wd,path,plotMode)
		return Ryx
	except ValueError as err:
		print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return None
			

def main():


		Fs = 20e6
		Fr = 2400e6
		Ryx = None
		print("transmitting...")
		Ryx = routine_stat(Fs,Fr,plotMode=True)

		print("done")
		print(Ryx)
	


if __name__ == '__main__':
    main()
