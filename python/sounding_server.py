# TX, only task is to wait for a signal to start to transmitt and then send back ruido data
import socket
import paramiko
import os
import sys

import threading
from whiteNoiseGen import whiteNoiseGen
from sondeoWithoutGui import *
from dataProcess import dataProcess
from sondeoTx import *





ip = '192.168.10.4'
#ip = '192.168.10.3'
name = "udg"
#name = "grzechu"

HOST ='192.168.10.3'              # Symbolic name meaning all available interfaces
#HOST = '127.0.0.1'   
PORT = 50007             # Arbitrary non-privileged port
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


message = "" # take input
shut = False
pozycja = 0


while message.lower().strip() != 'narazie' and not shut:

	data = conn.recv(1024).decode()  # receive response

	if data == "start":
		
        	sondeoTx()
        	message = "done" 
        	conn.send(message.encode())
        	os.system("scp -i ~/.ssh/id_rsa.pub /dev/shm/ruido* "+name +"@"+ip+":/dev/shm/")
        	print("udalo sie")
        	shut=True




conn.close()  # close the connection

#try: 
#	while True:
	#	print("co jest stefan")
#		conn.close()
	#	sys.exit(0)
#except KeyboardInterrupt:
#	print("mam cie")