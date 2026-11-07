from http import client
import sys, os # sys - acces to cmd line , os - loc of files/folders
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "common")) # Append the common directory to the Python path
import random

#---modules---
import socket, hashlib    
from protocol import send_msg 
from protocol import (CHUNK_SIZE, send_chunk, recv_chunk, pack_numbers,
                      unpack_numbers, END_MARK, RESEND_MARK, DONE_MARK)

filename = sys.argv[1]  # it retrieves the testfile/small.bin by providing by cmd line

with open(filename, "rb") as f:            # rb = read binary
    data = f.read()     #reads the entire file into ram

print("Sending", len(data), "bytes") # calculates the file size
print("MD5:", hashlib.md5(data).hexdigest())  #calculates and gives a reference hash of og file to compare

"""client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # AF - address family (IPv4) , sock_stream - socket type
client.connect(("127.0.0.1", 5001))    #sender initiate connection to the receiver's IP address & port"""

clientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientA.connect(("127.0.0.1", 5001))
clientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientB.connect(("127.0.0.1", 5001))
paths = [clientA, clientB]

#send_msg(client, data)   #transfers the message (tcp conn, file stored in ram)

chunks = []
chunk_no = 0
for start in range(0, len(data), CHUNK_SIZE):
    chunks.append((chunk_no, data[start : start + CHUNK_SIZE]))    #divides the file into chunks of 1024 bytes and stores them in a list along with their chunk number
    chunk_no += 1

if "--shuffle" in sys.argv:    #checks if --shuffle is in the cmd line argumments, if yes then it shuffles the chunks before sending them to the receiver
    random.shuffle(chunks)
    print("Shuffled. First chunk numbers sent:", [c[0] for c in chunks[:5]]) #get the first 5 chunk numbers from the shuffled list.


#----Intentionall drop chunk to simulate packet loss----
dropped = set()
if "--drop" in sys.argv:
    dropped = {n for n in range(len(chunks)) if n % 7 == 3}     #skip chucks 3,10,17....
    print("Skipping chunks:", sorted(dropped)[:10])

for chunk_no, chunk in chunks:
    if chunk_no in dropped:
        continue
    send_chunk(paths[chunk_no % 2], chunk_no, chunk) # even chunk no. -> clientA, odd chunk no. -> clientB

def send_end():
    for p in paths:
        send_chunk(p, END_MARK, pack_numbers([len(chunks)]))  #send packs expected chunks for receiver to check for missing chunks

send_end()  #send the END_MARK to both clients to indicate that all chunks have been sent
chunk_by_no = dict(chunks)

#---feedback loop---
while True:
    kind, payload = recv_chunk(paths[0])      # wait for the receiver's answer
    if kind == DONE_MARK:
        print("Receiver confirmed: all chunks received")
        break
    if kind == RESEND_MARK:
        missing = unpack_numbers(payload)
        print("Resending chunks:", missing[:10])
        for n in missing:
            send_chunk(paths[n % 2], n, chunk_by_no[n])   #deciding the client to send based on the chuck number (even -> clientA, odd -> clientB)
        send_end()
    else:
        break   

print("Sent", len(chunks), "chunks")
clientA.close()
clientB.close()