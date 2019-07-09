# Echo server program
import socket

HOST = '192.168.10.4'                 # Symbolic name meaning all available interfaces
PORT = 50008              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

response ="ccac"
message = raw_input(" -> ")  # 
conn.send(message.encode())  # send message

while message.lower().strip() != 'zamknij':
        # receive data stream. it won't accept data packet greater than 1024 bytes
	response = conn.recv(1024).decode()

	print("from connected user: " + str(response))
	message = raw_input(' -> ')
	conn.send(message.encode())  # send data to the client


conn.close()  # close the connection