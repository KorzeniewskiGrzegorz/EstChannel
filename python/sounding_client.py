# RX, where the data is generated and processed
import socket
import paramiko
import os
import traceback

import threading
from whiteNoiseGen import whiteNoiseGen
from sondeoWithoutGui import *
from dataProcess import dataProcess
from sondeoRx import *
from scipy.ndimage.interpolation import shift

def sounding_client(Fs,
					bw=1.5e6,
					offman =0,
					plotMode=False,
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

	print '<'*80 
	print '<'*80 
	print "INIT"
	whiteNoiseGen(Fs)

	######################

	
	print("Sending generated noise ..."),
	os.system("scp -i ~/.ssh/id_rsa.pub /dev/shm/IPulse.dat /dev/shm/QPulse.dat "+ name +"@"+ip+":/dev/shm/")
	print("Done")

	response =""
	message = "start"  # 
	conn.send(message.encode())  # send message
	shut = False

	sondeoRx(Fs,bw)

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
		Ryx = dataProcess(Fs,offman=offman,wd=wd,path=path,offsetTime = 0.5,offsetThreshold = 0.0035,plotMode=plotMode)
		return Ryx
	except ValueError as err:
		print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return None
			

def main():


		Fs = 20e6
		Ryx = None
		print("transmitting...")
		Ryx = sounding_client(Fs)

		print("done")
		print(Ryx)
	


if __name__ == '__main__':
    main()
