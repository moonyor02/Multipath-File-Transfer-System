import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "common"))

import socket
import hashlib
from protocol import send_msg

# File to send
filename = sys.argv[1]

# Read the file in binary mode
with open(filename, "rb") as f:
    data = f.read()

# Calculate MD5 checksum
checksum = hashlib.md5(data).hexdigest()

# Create TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to receiver
client.connect(("127.0.0.1", 5001))

print("Connected to receiver!")

# Send file data
send_msg(client, data)

print("File sent successfully!")
print("Sent:", len(data), "bytes")
print("MD5:", checksum)

# Close connection
client.close()