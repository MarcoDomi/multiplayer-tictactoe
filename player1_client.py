import socket
from gameboard import game_state

def get_msg(sock):
    full_msg = ''  #string used to store the full message
    new_msg = True #this is a new_msg so set to true

    while True:
        HEADERSIZE = 10     #length of header being sent from server is 10 characters
        msg = sock.recv(16).decode('utf-8') #recieve 16 bytes of msg at a time 

        if new_msg:                         #if msg is a new message
            msglen = int(msg[:HEADERSIZE])  #read up to the end of the header #convert the msg_length value in the header string to int
            new_msg = False                 #message is no longer new so set to false
        
        full_msg += msg   #append the recieved characters to the full_msg string

        if len(full_msg) - HEADERSIZE == msglen: #if full_msg lenth minus headerlength is equal to value found in the header
            return full_msg[HEADERSIZE:]         #return msg starting after end of header 

#get the current state of game and the current turn
def get_game_data(sock):
    board = get_msg(sock)       #get game board + game status
    extra_data = board[-2:]     #remove the game_status and current_turn from game board string
    game_value, turn_value = int(extra_data[0]), int(extra_data[1]) #store values for game status and current turn
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
print(msg)#print welcome message
valid_turn = int(msg[-1]) #stores the valid turn for this player

game_status = game_state.IN_PROGRESS         #inital status of game is IN_PROGRESS
while game_status == game_state.IN_PROGRESS: #if status of the game is IN_PROGRESS keep looping
    game_status, current_turn = get_game_data(s) #get game_status and current_turn

    if current_turn == valid_turn:   #if current_turn matches w/ this player then execute follwing statements
        choice = input("Choose a location:")  #get a location from user
        s.send(bytes(choice, 'utf-8'))        #send location choice
        game_status, current_turn = get_game_data(s) #get updated game_status and current_turn

end_msg = s.recv(1024).decode('utf-8') #recieve the end msg sent from server
print(end_msg)