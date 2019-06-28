#from soundingModules import *
import threading
from whiteNoiseGen import whiteNoiseGen
from sondeoWithoutGui import *
from dataProcess import dataProcess

Fs = 20e6
path = '/dev/shm/'

calibrationOffsetTime = 1# calibration time [s] , corresponds to parameters of signal generation
offman = 15;
wd = 10; # window duration [us] for the correlation purpose
path = "/dev/shm/"



whiteNoiseGen(Fs)
print("###############################")
print("\n\n\n\n\n\n\n")


result_available = threading.Event()

thread = threading.Thread(target=blader, args=(result_available,))
thread.start()


print("###############################")
print("\n\n\n\n\n\n\n")
result_available.wait()

dataProcess(Fs,offman = offman)

