import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "common"))

import socket, hashlib
from protocol import recv_msg

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5001))
server.listen()
print("Waiting for sender...")

conn, addr = server.accept()
data = recv_msg(conn)                      # whole file in one message

with open("received.bin", "wb") as f:      # wb = write binary
    f.write(data)

print("Received", len(data), "bytes")
print("MD5:", hashlib.md5(data).hexdigest())

conn.close()
server.close()