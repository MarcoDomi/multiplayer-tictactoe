import socket

host = '127.0.0.1'

def accept_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()

    player_sock, addr = s.accept()
    print(f"Player connected at {addr}")
    return player_sock

port1 = 9090
port2 = 9091

while True:
    player1_sock = accept_connection(host, port1)
    player1_sock.send(bytes("welcome player 1","utf-8"))

    player2_sock = accept_connection(host, port2)
    player2_sock.send(bytes("welcome player 2", "utf-8"))

    player1_sock.close()
    player2_sock.close()
