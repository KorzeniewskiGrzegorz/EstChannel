#! /usr/bin/python

from threading import Timer
import threading
from sounding import *
from dcFilter import *

Fs = 20e6
bw = 1.5e6

result_available = threading.Event()
thread = threading.Thread(target=sounding, args=(Fs,bw,result_available,))
thread.start()
print("transmitting...")
result_available.wait()
print("done")

dc_filter()