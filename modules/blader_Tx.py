import os
import sys
import time
from threading import Timer
import threading

def txSet(Fr,Fs,bw):
	os.system("bladeRF-cli -d '*:serial=32a' -e \""+
        "set frequency tx "+str(Fr)+
        ";set samplerate tx "+str(Fs)+
	";set bandwidth tx "+str(bw)+
        ";tx config file=/dev/shm/tx.bin"+
        ";tx config repeat=2 delay=0"+
        ";tx start"+
        ";tx wait\"")

def blader_Tx(sr,fr,bw,e):

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
        e.set()
    start=time.time()  	
    txSet(fr,sr,bw)
    finish(e)
    

if __name__ == '__main__':
    
    Fs = 38e6
    Fr = 2.3e9
    bw = 28e6

    

    result_available = threading.Event()
    thread = threading.Thread(target=blader_Tx, args=(Fs,Fr,bw,result_available,))
    thread.start()
    print("transmitting...")
    result_available.wait()
