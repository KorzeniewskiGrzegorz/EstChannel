# RX, where the data is generated and processed
import socket
import paramiko
import os
import sys
import traceback

import threading
from whiteNoiseGen import whiteNoiseGen
from dataProcess import dataProcess
from blader_Rx import *
from dcFilter import dcFilter 
from scipy.ndimage.interpolation import shift

def routine_remote(Fs,
					Fr = 2.4e6,
					bw=1.5e6,
					offman =0,
					plotMode=False,
					path = '/dev/shm/',
					wd = 10,
					):

	#os.system("bladeRF-cli -d '*:serial=179' -e \"set smb_mode input\"")

	HOST = '192.168.0.6'         # The remote host
	#HOST = '127.0.0.1'   
	PORT = 50008        # The same port as used by the server
	#ip = '192.168.10.4'
	ip = HOST
	name = "pi"
	#name = "udg"

	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	conn.connect((HOST, PORT))

	print '<'*80 
	print '<'*80 
	print "INIT"
	#whiteNoiseGen(Fs)

	######################

	
	print("Sending generated noise ..."),
	#os.system("scp -i ~/.ssh/id_rsa.pub /dev/shm/tx.bin "+ name +"@"+ip+":/dev/shm/")
	print("Done")

	response =""
	message = "start;Fs:{0},Fr:{1},BW:{2}".format(Fs,Fr,bw)  # 
	conn.send(message.encode())  # send message
	shut = False


	result_available = threading.Event()
	thread = threading.Thread(target=blader_Rx, args=(Fs,Fr,bw,result_available,))
	thread.start()
	print("transmitting...")
	result_available.wait()

	while message.lower().strip() != 'zamknij' and not shut:
	        # receive data stream. it won't accept data packet greater than 1024 bytes
		response = conn.recv(1024).decode()
		print("                               from connected user: " + str(response))

		if response == "done":
			shut = True



	conn.close()  # close the connection

	dcFilter()


	print("processing data ...")


	
	try:
		Ryx = dataProcess(Fs,wd,path,plotMode)
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
		Ryx = routine_remote(Fs)

		print("done")
		print(Ryx)
	


if __name__ == '__main__':
    main()
