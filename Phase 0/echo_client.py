import socket
from protocol import recv_msg, send_msg

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5001))       #TCP 3 way handshake is done here.

while True:
    msg = input("Enter a message to send to the server: ")
    if not msg:
        break
    send_msg(client, msg.encode())
    reply = recv_msg(client)
    print("Server said:", reply.decode())

client.close()