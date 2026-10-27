import socket
from time import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5001))   #claimed port 5001 for server

server.listen()                   #told os to accept for incoming connections
print("Waiting for a client...")

conn, addr = server.accept()     #paused the program until a client connects.
print("Connected by", addr)

while True:
    data = conn.recv(1024) # read the data
    if not data:
        break
    print("Got:", data) # prints the data recieved.
    conn.sendall(data) # sends the data back

conn.close()
server.close()