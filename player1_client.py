import socket
def print_msg(sock):
    headersize = 10
    msg = sock.recv(1024).decode('utf-8')
    msglen = int(msg[:headersize])
    print(msglen)

host = '127.0.0.1'
port = 9090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

print(s.recv(1024).decode('utf-8'))

