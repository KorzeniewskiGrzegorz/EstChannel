# TX, only task is to wait for a signal to start to transmitt and then send back ruido data
import socket

import os
import sys
sys.path.insert(1, '/home/grzechu/git/EstChannel/modules')
import threading
from blader_Tx import blader_Tx


def server_work(s,name,Fs =20e6):

	while True:
		
		print("waiting for connection ...")

		conn, addr = s.accept()
		print 'Connected by', addr




		message = "" # take input
		shutConn = False



		while not shutConn:

			data = conn.recv(1024).decode()  # receive response

			if "start" in data:

				strs = data.split(";")[1]

				parms = strs.split(",")

				Fs = float(parms[0].split(":")[1])
				Fr = float(parms[1].split(":")[1])
				bw = float(parms[2].split(":")[1])

				result_available = threading.Event()

				thread = threading.Thread(target=blader_Tx, args=(Fs,Fr,bw,result_available,))
				thread.start()

	        	result_available.wait()


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
		server_work(s,name,Fs)
	
	except KeyboardInterrupt:
		print("\nserver shutted down")
		s.close() 

	s.close() # close server



if __name__ == '__main__':
	
	sounding_server()




    

