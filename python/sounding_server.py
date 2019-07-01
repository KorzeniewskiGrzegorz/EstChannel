# Echo server program
import socket

import threading
from whiteNoiseGen import whiteNoiseGen
from sondeoWithoutGui import *
from dataProcess import dataProcess
from sondeoRx import *

HOST = '192.168.10.4'                 # Symbolic name meaning all available interfaces
#HOST = '127.0.0.1'   
PORT = 50008              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr


Fs = 20e6
path = '/dev/shm/'
calibrationOffsetTime = 1# calibration time [s] , corresponds to parameters of signal generation
offman = 15;
wd = 10; # window duration [us] for the correlation purpose


#whiteNoiseGen(Fs)
#print("###############################")
#print("\n\n\n\n\n\n\n")



response =""
message = "start"  # 
conn.send(message.encode())  # send message
shut = False

sondeoRx()

while message.lower().strip() != 'zamknij' and not shut:
        # receive data stream. it won't accept data packet greater than 1024 bytes
	response = conn.recv(1024).decode()
	print("from connected user: " + str(response))

	if response == "done":
		shut = True



conn.close()  # close the connection