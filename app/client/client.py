#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345             # Reserve a port for your service.

s.connect((host, port))
##print(s.recv(1024))

while True:
    data = s.recv(1024)
    print("RECIEVED:" , data)
    data = raw_input( "SEND DATA TO FLASK webSocketIo_:")
    s.send(data)
