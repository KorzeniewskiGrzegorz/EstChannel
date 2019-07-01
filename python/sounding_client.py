# RX, where the data is generated and processed
import socket

HOST = '192.168.10.3'         # The remote host
#HOST = '127.0.0.1'   
PORT = 50008              # The same port as used by the server
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))




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
