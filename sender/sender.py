import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "common"))

import socket, hashlib
from protocol import send_msg

filename = sys.argv[1]                     # file name given on the command line

with open(filename, "rb") as f:            # rb = read binary
    data = f.read()

print("Sending", len(data), "bytes")
print("MD5:", hashlib.md5(data).hexdigest())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5001))
send_msg(client, data)
client.close()