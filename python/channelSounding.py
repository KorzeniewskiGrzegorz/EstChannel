from soundingModules import *
import threading

Fs = 20e6
path = '/dev/shm/'


whiteNoiseGen(Fs)
print("###############################")
print("\n\n\n\n\n\n\n")


result_available = threading.Event()

thread = threading.Thread(target=blader, args=(result_available,))
thread.start()


print("###############################")
print("\n\n\n\n\n\n\n")
result_available.wait()

dataProcess(Fs)

