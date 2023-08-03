import socket

host = '127.0.0.1'
port = 9090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

print(s.recv(1024).decode('utf-8'))
