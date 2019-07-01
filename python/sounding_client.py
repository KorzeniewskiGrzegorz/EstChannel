# RX, where the data is generated and processed
import socket
import paramiko

import threading
from whiteNoiseGen import whiteNoiseGen
from sondeoWithoutGui import *
from dataProcess import dataProcess
from sondeoRx import *
from cryptography.fernet import Fernet

HOST = '192.168.10.3'         # The remote host
#HOST = '127.0.0.1'   
PORT = 50007             # The same port as used by the server
ipUdg = '192.168.10.4'
ipGrzechu = '192.168.10.3'

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))

Fs = 20e6
path = '/dev/shm/'
calibrationOffsetTime = 1# calibration time [s] , corresponds to parameters of signal generation
offman = 15;
wd = 10; # window duration [us] for the correlation purpose

whiteNoiseGen(Fs)

######################



text_file = open("/home/udg/Escritorio/klucz.txt", "r")
key=text_file.read()

with open('/home/udg/Escritorio/hasloDom.bin', 'rb') as file_object:
    for line in file_object:
        encryptedpwd = line


cipher_suite = Fernet(key)
unciphered_text = (cipher_suite.decrypt(encryptedpwd))

ssh_client =paramiko.SSHClient() 
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
ssh_client.connect(hostname=ipGrzechu,username='grzechu',password=unciphered_text)

ftp_client=ssh_client.open_sftp() 
ftp_client.put('/dev/shm/IPulse.dat','/dev/shm/IPulse.dat') 
ftp_client.put('/dev/shm/QPulse.dat','/dev/shm/QPulse.dat') 
ftp_client.close()
###





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
