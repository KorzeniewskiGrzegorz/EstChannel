# RX, where the data is generated and processed
import socket
import paramiko
import os

import threading
from whiteNoiseGen import whiteNoiseGen
from sondeoWithoutGui import *
from dataProcess import dataProcess
from sondeoRx import *
from cryptography.fernet import Fernet

HOST = '192.168.10.3'         # The remote host
#HOST = '127.0.0.1'   
PORT = 50007             # The same port as used by the server
#ip = '192.168.10.4'
ip = '192.168.10.3'
name = "grzechu"
#name = "udg"

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))

Fs = 20e6
path = '/dev/shm/'
calibrationOffsetTime = 1# calibration time [s] , corresponds to parameters of signal generation
offman = 15;
wd = 10; # window duration [us] for the correlation purpose

whiteNoiseGen(Fs)

######################


os.system("scp -i ~/.ssh/id_rsa.pub /dev/shm/IPulse.dat /dev/shm/QPulse.dat "+ name +"@"+ip+":/dev/shm/")


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
