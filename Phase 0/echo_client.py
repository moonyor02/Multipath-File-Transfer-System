import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 5001))       #TCP 3 way handshake is done here.

client.sendall(b"hello")

reply = client.recv(1024) #same as server.
print("Server said:", reply) #same as server.

client.close()