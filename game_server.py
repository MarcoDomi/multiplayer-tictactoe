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

    #create game
    game = tictactoe_game()

    #player 1 turn
    game.current_player = player1          #set current_player to player 1

    game_status = game.win_status          #set current status of the game
    msg = game.game_board.return_board()   #return a string that contains the game board
    msg += str(game_status.value)          #append the value of the current game status to end of game board string
    msg = create_header(msg) + msg         #prepend header to msg that contains the game board string
    player1_sock.send(bytes(msg, 'utf-8')) #send board + win status to player 1

    p1_choice = int(player1_sock.recv(16).decode('utf-8')) #TODO change to buffer to 1 #get player 1 choice
    print(p1_choice, type(p1_choice)) #NOTE DELETE
    feedback_msg = game.place_symbol(p1_choice)#get feedback msg 
    #feedback_msg = create_header(feedback_msg) + feedback_msg
    print(game.win_status) #NOTE DELETE
    game.check_winner() #check if game has a winner
    print(game.win_status) #NOTE DELETE
    game_status = game.win_status #set current status of game again
    msg = game.game_board.return_board() #get gameboard after placing a symbol
    msg += str(game_status.value)
    msg = create_header(msg) + msg
    player1_sock.send(bytes(msg, 'utf-8'))

    #close connections
    player1_sock.close()
    player2_sock.close()
