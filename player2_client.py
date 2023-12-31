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
            new_msg = False
        
        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            return full_msg[HEADERSIZE:]
        
def get_game_data(sock):
    board = get_msg(sock)       #get game board + game status
    extra_data = board[-2:]
    game_value, turn_value = (int(extra_data[0]), int(extra_data[1])) #store values for game status and current turn
    board = board[:-2]          #remove the last two characters from board string #the last characters are status of the game and current turn
    print(board)

    return game_state(game_value), turn_value #do not convert turn_value to its respective enum-name

host = '127.0.0.1'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    port = 9090
    s.connect((host, port))
    
except:
    port = 9091
    s.connect((host, port))
    
msg = s.recv(1024).decode('utf-8')
print(msg) #print welcome message
valid_turn = int(msg[-1]) #stores the valid turn for this player

game_status = game_state.IN_PROGRESS
while game_status == game_state.IN_PROGRESS:
    game_status, current_turn = get_game_data(s)
    
    if current_turn == valid_turn:
        choice = input("Choose a location:")
        s.send(bytes(choice, 'utf-8'))
        game_status, current_turn = get_game_data(s) 

end_msg = s.recv(1024).decode('utf-8')
print(end_msg)