import socket
from gameboard import tictactoe_game, game_state, player

def accept_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    player_sock, addr = s.accept()
    print(f"Player connected at {addr}")
    return player_sock

#create a header that is prepended to msg to be send
def create_header(msg):
    headersize = 10  #max msg is a billion bytes so the number '1 billion' can be represented using 10 characters so the header is 10 characters long
    header = f"{len(msg):<{headersize}}"  #use the msg length value with string formating to create a header #msg length is left aligned with spaces to right
    return header

#send the current board and the games current status to player
def send_current_game(player_sock, game, current_turn):
    msg = game.game_board.return_board()    #return a string that contains the game board
    msg = msg + str(game.win_status.value) + str(current_turn.value) #append the value of the current game status and current turn to game board string
    msg = create_header(msg) + msg          #prepend header to msg that contains the game board string
    player_sock.send(bytes(msg, 'utf-8'))   #send board + win status to player 1

#take a player location choice and attempt to place it on board and check for winner
def play_game(player_sock, game):
    choice = int(player_sock.recv(16).decode('utf-8')) #TODO change to buffer to 1 #get player 1 choice
    feedback_msg = game.place_symbol(choice)           #get feedback msg for error handling #TODO implement error handling
    game.check_winner()   #check if game has a winner

#send game result messages to both player at end of game
def send_end_msg(p1_sock, p2_sock, msg1, msg2):
    p1_sock.send(bytes(msg1,'utf-8'))
    p2_sock.send(bytes(msg2,'utf-8'))

host = '127.0.0.1'
port1 = 9090
port2 = 9091

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
    game.current_player = player1    #set current_player to player 1
    game_status = game.win_status    #set current status of the game
    
    turn = player1
    while game_status == game_state.IN_PROGRESS: 
        #player 1 turn
        if turn == player1:
            game.current_player = player1               #set current_player to player1
            send_current_game(player1_sock, game, turn) #send the game and the current turn to be processed and sent
            
            play_game(player1_sock, game)               #recieve a location for symbol from player and place it on board
            game_status = game.win_status               #set current status of game
            send_current_game(player1_sock, game, turn) #send the updated game and current turn the player

            if game_status != game_state.IN_PROGRESS:        #if current player wins then the opposing player must be notified immediately
                send_current_game(player2_sock, game, turn)  #send the winning board, game_status and current_turn to the opposing player

            turn = player2
        #player 2 turn
        elif turn == player2:
            game.current_player = player2
            send_current_game(player2_sock, game, turn)
            
            play_game(player2_sock, game)
            game_status = game.win_status
            send_current_game(player2_sock, game, turn)

            if game_status != game_state.IN_PROGRESS:
                send_current_game(player1_sock, game, turn)

            turn = player1
    
    if game_status == game_state.DRAW: #if game is a DRAW  send same msg to both players
        msg = "IT'S A DRAW"
        send_end_msg(player1_sock, player2_sock, msg, msg)
    else:
        win_msg = "YOU WIN"
        lose_msg = "YOU LOSE"
        if game.current_player == player1: #send a win and loss msg to either player depending on who won
            send_end_msg(player1_sock, player2_sock, win_msg, lose_msg)
        else:
            send_end_msg(player1_sock, player2_sock, lose_msg, win_msg)

    #close connections
    player1_sock.close()
    player2_sock.close()