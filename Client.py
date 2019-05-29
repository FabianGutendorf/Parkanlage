import socket
import sqlite3

HOST = '127.0.0.1'
PORT = 65432  

# Python Socket Try

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)

# print('Received', repr(data))


# Python SQLite Handling
conn = sqlite3.connect('Parkanlage.db')
c = conn.cursor()


for row in c.execute("SELECT * FROM Parker"):
    print(row)


# Python Socket


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'stop')
#     data = s.recv(1024)

# print('Received', repr(data))