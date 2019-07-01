# TX, only task is to wait for a signal to start to transmitt and then send back ruido data
import socket

import threading
from whiteNoiseGen import whiteNoiseGen
from sondeoWithoutGui import *
from dataProcess import dataProcess
from sondeoRx import *

HOST = '192.168.10.3'                 # Symbolic name meaning all available interfaces
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

message = "" # take input
shut = False
pozycja = 0


while message.lower().strip() != 'narazie' and not shut:

	data = s.recv(1024).decode()  # receive response

	print('Received from client: ' + data)  # show in terminal
	if data == "start":
		
	sondeoTx()


	else:
		print("nie rozumiem, rozlaczam sie")
		shut = True




conn.close()  # close the connection