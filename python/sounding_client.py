# RX, where the data is generated and processed
import socket
import paramiko
import os

import threading
from whiteNoiseGen import whiteNoiseGen
from sondeoWithoutGui import *
from dataProcess import dataProcess
from sondeoRx import *


def sounding_client(Fs,
					path = '/dev/shm/',
					wd = 10,
					plotMode=True):

	#os.system("bladeRF-cli -d '*:serial=179' -e \"set smb_mode input\"")

	HOST = '192.168.10.2'         # The remote host
	#HOST = '127.0.0.1'   
	PORT = 50007             # The same port as used by the server
	#ip = '192.168.10.4'
	ip = '192.168.10.2'
	name = "gregor"
	#name = "udg"

	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	conn.connect((HOST, PORT))


	whiteNoiseGen(Fs)

	######################


	os.system("scp -i ~/.ssh/id_rsa.pub /dev/shm/IPulse.dat /dev/shm/QPulse.dat "+ name +"@"+ip+":/dev/shm/")


	response =""
	message = "start"  # 
	conn.send(message.encode())  # send message
	shut = False

	sondeoRx(Fs)

	while message.lower().strip() != 'zamknij' and not shut:
	        # receive data stream. it won't accept data packet greater than 1024 bytes
		response = conn.recv(1024).decode()
		print("from connected user: " + str(response))

		if response == "done":
			shut = True




		 

	conn.close()  # close the connection
	print("\n\n\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("processing data ...")

	Ryx = dataProcess(Fs,offman=0,wd=wd,path=path,offsetTime = 0.5,offsetThreshold = 0.004)

	

def main():
	Fs = 10e6 #Sample freq
	R = 0.99; # ratio, the same as in generator script
	calibrationOffsetTime = 1# calibration time [s] , corresponds to parameters of signal generation
	offman = 0;
	wd = 10; # window duration [us] for the correlation purpose
	path = "/dev/shm/"

	sounding_client(Fs,	plotMode=True)


if __name__ == '__main__':
    main()
