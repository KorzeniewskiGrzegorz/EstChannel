# Echo client program
import socket

HOST = '127.0.0.1'         # The remote host
PORT = 50008              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

message = "" # take input

while message.lower().strip() != 'narazie':

	data = s.recv(1024).decode()  # receive response

	print('Received from server: ' + data)  # show in terminal

	message = raw_input(" -> ")  # again take input
	s.send(message.encode()) 

s.close()  # close the connection
