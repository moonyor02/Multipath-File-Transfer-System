import sys, os # sys - acces to cmd line , os - loc of files/folders
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "common")) # Append the common directory to the Python path

#---modules---
import socket, hashlib    
from protocol import send_msg 
from protocol import CHUNK_SIZE, send_chunk

filename = sys.argv[1]  # it retrieves the testfile/small.bin by providing by cmd line

with open(filename, "rb") as f:            # rb = read binary
    data = f.read()     #reads the entire file into ram

print("Sending", len(data), "bytes") # calculates the file size
print("MD5:", hashlib.md5(data).hexdigest())  #calculates and gives a reference hash of og file to compare

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # AF - address family (IPv4) , sock_stream - socket type
client.connect(("127.0.0.1", 5001))    #sender initiate connection to the receiver's IP address & port

#send_msg(client, data)   #transfers the message (tcp conn, file stored in ram)

chunk_no = 0
for start in range(0, len(data), CHUNK_SIZE):
    send_chunk(client, chunk_no, data[start : start + CHUNK_SIZE])
    chunk_no += 1
print("Sent", chunk_no, "chunks")
client.close()