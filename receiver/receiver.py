
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "common"))

import socket, hashlib
from protocol import recv_msg

# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to localhost and port 5001
server.bind(("127.0.0.1", 5001))

# Listen for connection
server.listen(1)

print("Waiting for sender...")

# Accept connection
conn, addr = server.accept()

print("Connected by:", addr)

# Receive file data
data = recv_msg(conn)

# Save received file
#filename = "received_file"

#with open(filename, "wb") as f:
 #   f.write(data)


# Save received file
filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "received_file.txt"
)

with open(filename, "wb") as f:
    f.write(data)

print("File saved at:", filename)


# Calculate MD5 checksum
checksum = hashlib.md5(data).hexdigest()

print("File received successfully!")
print("Received:", len(data), "bytes")
print("MD5:", checksum)
print("Saved as:", filename)

conn.close()
server.close()
