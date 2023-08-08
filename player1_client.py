import socket
from gameboard import game_state, player

def get_msg(sock):
    full_msg = ''
    new_msg = True

    while True:
        HEADERSIZE = 10
        msg = sock.recv(16).decode('utf-8')

        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        
        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            return full_msg[HEADERSIZE:]

def get_game_data(sock,game_status):
    board = get_msg(sock)       #get game board + game status
    extra_data = board[-2:]
    game_status = int(board[-1])#store last character as game status
    board = board[:-1]          #remove the last character from board string #the last character is the status of the game
    print(board)

    return game_state(game_status)

host = '127.0.0.1'
port = 9090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print(s.recv(1024).decode('utf-8')) #print welcome message

game_status = game_state.IN_PROGRESS
while game_status == game_state.IN_PROGRESS:
    game_status = get_game_data(s, game_status)

    choice = input("Choose a location:")
    s.send(bytes(choice, 'utf-8')) #send location choice

    game_status = get_game_data(s, game_status)