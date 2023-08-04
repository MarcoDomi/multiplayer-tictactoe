import socket
from gameboard import tictactoe_game, win_status, player

host = '127.0.0.1'

def accept_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()

    player_sock, addr = s.accept()
    print(f"Player connected at {addr}")
    return player_sock

def create_header(msg):
    headersize = 10
    header = f"{len(msg):<{headersize}}"
    return header

port1 = 9090
port2 = 9091
create_header("hello")
while True: 
    #NOTE make it so either client could connect first
    player1_sock = accept_connection(host, port1)
    player1 = player.P1
    player1_sock.send(bytes("welcome player 1","utf-8"))

    player2_sock = accept_connection(host, port2)
    player2 = player.P2
    player2_sock.send(bytes("welcome player 2", "utf-8"))

    game = tictactoe_game()
    game.current_player = player1

    msg = game.game_board.return_board()
    msg = create_header(msg) + msg
    player1_sock.send(bytes(msg, 'utf-8'))

    player1_sock.close()
    player2_sock.close()
