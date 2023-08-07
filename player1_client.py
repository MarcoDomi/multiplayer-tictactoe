import socket
from gameboard import game_state

def get_msg(sock):
    full_msg = ''
    new_msg = True

    while True:
        HEADERSIZE = 10
        msg = sock.recv(16).decode('utf-8')

        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            #print("Message length:",msglen)
            new_msg = False
        
        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            return full_msg[HEADERSIZE:]

host = '127.0.0.1'
port = 9090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print(s.recv(1024).decode('utf-8')) #print welcome message

game_status = game_state.IN_PROGRESS
while game_status == game_state.IN_PROGRESS:
    board = get_msg(s) #get game board + game status
    game_status = int(board[-1])#store last character as game status
    board = board[:-1] #remove the last character from board string #the last character is the status of the game
    print(board)
    print(game_state(game_status)) #NOTE delete later

    choice = input("Choose a location:")
    s.send(bytes(choice, 'utf-8')) #send location choice

    board = get_msg(s)
    game_status = int(board[-1])
    board = board[:-1]
    print(board)
    print(game_status) #NOTE delete later