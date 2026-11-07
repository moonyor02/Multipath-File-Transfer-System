
# framing protocol for sending and receiving messages over a socket
import struct

def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            break
        data += chunk
    return data

def send_msg(sock, data):
    header = struct.pack(">I", len(data))  #len = 5 the [00 00 00 05] [h e l l o]
    sock.sendall(header + data)   #label infront message with length of message in bytes.

def recv_msg(sock):
    header = recv_exact(sock, 4) # returns 4 raw bytes which is length of the message
    if len(header) < 4:          # the other side disconnected and the header is less than 4
        return b""
    length = struct.unpack(">I", header)[0] #turn label into number
    return recv_exact(sock, length) #return the bytes of the msg which is the main msg


CHUNK_SIZE = 1024   # 1KB = 1024 bytes

def send_chunk(sock, chunk_no, data):
    send_msg(sock, struct.pack(">I", chunk_no) + data)    #converts the chunk number into 4 bytes and sends it along with the data

def recv_chunk(sock):
    payload = recv_msg(sock)   #gets the entire chunk (4 bytes of chunk number + data) and returns it as payload
    if not payload:
        return None, None
    return struct.unpack(">I", payload[:4])[0], payload[4:] #first convert the first 4 bytes into chunk number and return the rest of the payload as data


END_MARK    = 0xFFFFFFFF   # sender -> receiver, data = total chunk count
RESEND_MARK = 0xFFFFFFFE   # receiver -> sender, data = missing chunk numbers
DONE_MARK   = 0xFFFFFFFD   # receiver -> sender, nothing is missing

def pack_numbers(nums):
    return b"".join(struct.pack(">I", n) for n in nums)   #list of each number -> 4 bytes

def unpack_numbers(data):
    return [struct.unpack(">I", data[i:i+4])[0] for i in range(0, len(data), 4)]   #reverse of pack_numbers, takes the data and returns a list of numbers