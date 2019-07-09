# TX, only task is to wait for a signal to start to transmitt and then send back ruido data
import socket

import os
import sys

import threading
from sondeoTx import *


def server_work(s,Fs,name):


	while True:
		
		print("waiting for connection ...")

		conn, addr = s.accept()
		print 'Connected by', addr




		message = "" # take input
		shutConn = False



		while not shutConn:

			data = conn.recv(1024).decode()  # receive response

			if data == "start":
				
		        	sondeoTx(Fs)
		        	message = "sending tx data ..." 
		        	conn.send(message.encode())
		        	os.system("scp -i ~/.ssh/id_rsa.pub /dev/shm/ruido* "+name +"@"+str(addr[0])+":/dev/shm/")
		        	message = "done" 
		        	conn.send(message.encode())
		        	print("Finish")
		        	
		        	shutConn=True




		conn.close()  # close the connection


def sounding_server():
	os.system("bladeRF-cli -d '*:serial=32a' -e \"set smb_mode input\"")

	Fs = 20e6
	path = '/dev/shm/'
	calibrationOffsetTime = 1# calibration time [s] , corresponds to parameters of signal generation
	offman = 15;
	wd = 10; # window duration [us] for the correlation purpose

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

	try:
		server_work(s,Fs,name)
	
	except KeyboardInterrupt:
		print("\nserver shutted down")
		s.close() 

	s.close() # close server



if __name__ == '__main__':
	
	sounding_server()




    

