import os
import sys
import time
from threading import Timer
import threading


def txWork(Fr,Fs,bw):
	os.system("bladeRF-cli -d '*:serial=32a' -e \"set frequency tx"+Fr+"\"")
	os.system("bladeRF-cli -d '*:serial=32a' -e \"set samplerate tx"+Fs+"\"")
	os.system("bladeRF-cli -d '*:serial=32a' -e \"set bandwidth tx"+bw+"\"")
	os.system("bladeRF-cli -d '*:serial=32a' -e \"tx config file=/dev/shm/tx.sc16q11 format=bin\"")
	os.system("bladeRF-cli -d '*:serial=32a' -e \"tx config repeat=2 delay=0\"")
	os.system("bladeRF-cli -d '*:serial=32a' -e \"tx start\"")



def blader_Tx(sr,fr,bw,e):

    start=time.time()

    def finish(e):
        end = time.time()
        print "\n"
        print "%"*40
        print("transmission time: \t"+str(end-start)+"s")
        print("\tsamp rate: \t"+str(sr)+" samples/s")
        print("\tcarr freq: \t"+str(fr)+"Hz")
        print("\tbandwidth: \t"+str(bw)+"Hz")
        print "%"*40
        print "\n"
        tb.stop()
        tb.wait()
        e.set()
  	
    txWork(fr,sr,bw)


    t = Timer(3, finish, [e])
    t.start() # after 30 seconds, "hello, world" will be printed    


if __name__ == '__main__':
    
    Fs = 38e6
    Fr = 2.17e9
    bw = 28e6

    

    result_available = threading.Event()
    thread = threading.Thread(target=blader_Tx, args=(Fs,Fr,bw,result_available,))
    thread.start()
    print("transmitting...")
    result_available.wait()