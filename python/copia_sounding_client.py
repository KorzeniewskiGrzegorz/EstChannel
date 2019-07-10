# RX, where the data is generated and processed
import socket
import paramiko
import os

import threading
from whiteNoiseGen import whiteNoiseGen
from sondeoWithoutGui import *
from dataProcess import dataProcess
from sondeoRx import *
import Queue



def sounding_client(Fs,
					event,
					plotMode,
					outputQueue,
					path = '/dev/shm/',
					wd = 10,
					):

	#os.system("bladeRF-cli -d '*:serial=179' -e \"set smb_mode input\"")

	HOST = '192.168.10.3'         # The remote host
	#HOST = '127.0.0.1'   
	PORT = 50007         # The same port as used by the server
	#ip = '192.168.10.4'
	ip = HOST
	name = "grzechu"
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

	
	try:
		Ryx = dataProcess(Fs,offman=0,wd=wd,path=path,offsetTime = 0.5,offsetThreshold = 0.004,plotMode=plotMode)
		outputQueue.put(Ryx)
		event.set() # event set
	except ValueError as err:
		print("Unexpected error:", sys.exc_info()[0])
		event.set() # event set
	

def main():

		Ryx = -1;
		myQueue = Queue.Queue()
		Fs = 20e6
		result_available = threading.Event()
		thread = threading.Thread(target=sounding_client, args=(Fs,result_available,False,myQueue))
		thread.start()
		print("transmitting...")
		result_available.wait()
		if myQueue.empty() is not True:
			Ryx = myQueue.get()

		print("done")
		print(Ryx)
	


if __name__ == '__main__':
    main()
