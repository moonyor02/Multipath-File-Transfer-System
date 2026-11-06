import sys, os # sys - acces to cmd line , os - loc of files/folders
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "common")) # Append the common directory to the Python path
import random

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

chunks = []
chunk_no = 0
for start in range(0, len(data), CHUNK_SIZE):
    chunks.append((chunk_no, data[start : start + CHUNK_SIZE]))    #divides the file into chunks of 1024 bytes and stores them in a list along with their chunk number
    chunk_no += 1

if "--shuffle" in sys.argv:    #checks if --shuffle is in the cmd line argumments, if yes then it shuffles the chunks before sending them to the receiver
    random.shuffle(chunks)
    print("Shuffled. First chunk numbers sent:", [c[0] for c in chunks[:5]]) #get the first 5 chunk numbers from the shuffled list.

for chunk_no, chunk in chunks:
    send_chunk(client, chunk_no, chunk)

print("Sent", len(chunks), "chunks")
client.close()