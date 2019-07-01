# Echo client program
import socket

HOST = '192.168.10.4'         # The remote host
#HOST = '127.0.0.1'   
PORT = 50008              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))





message = "" # take input
shut = False
pozycja = 0


while message.lower().strip() != 'narazie' and not shut:

	data = s.recv(1024).decode()  # receive response

	print('Received from server: ' + data)  # show in terminal
	if data == "start":
		
	sondeoTx()


	else:
		print("nie rozumiem, rozlaczam sie")
		shut = True




	 

s.close()  # close the connection
