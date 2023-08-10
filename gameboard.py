from enum import Enum
class game_state(Enum):
    IN_PROGRESS = 0
    WIN = 1
    DRAW = 2
    LOSS = 3

class player(Enum):
    P1 = 1
    P2 = 2

class tictactoe_board:
    def __init__(self):
        self.board = [[1,2,3], [4,5,6], [7,8,9]] #tictactoe board
        self.floor = '{:-^13}'.format('') #string of dashes that separate board rows
        self.wall = '{:^5}'.format('|')   #straight line w/ 2 spaces on e/ side
        self.BOARD_DIMENSION = 3          #dimension of board

    def return_board(self): 
        board_str = ""
        for i in range(self.BOARD_DIMENSION): 
            board_str = board_str + f"{self.board[i][0]}{self.wall}{self.board[i][1]}{self.wall}{self.board[i][2]}" #append a row of values w/ a wall btwn e/ value
            if i != self.BOARD_DIMENSION - 1: #if current row is not the last row
                board_str = board_str + '\n'  #append new line to current row in board string
                board_str = board_str + f"{self.floor}\n" #append a floor to board string
        return board_str
                
class tictactoe_game:
    def __init__(self):
        self.game_board = tictactoe_board()           #instantiate tictactoe_board object as embedded object
        self.symbol = { player.P1:'X', player.P2:'O'} #dict with players as key and symbol as value
        self. win_status = game_state.IN_PROGRESS     #set initial status of game as IN_PROGRESS
        self.current_player = player.P1               #current player is P1
        self.valid_coord_choices = {1:(0,0), 2:(0,1), 3:(0,2), #all valid locations on game board
                                    4:(1,0), 5:(1,1), 6:(1,2),
                                    7:(2,0), 8:(2,1), 9:(2,2)}
    #public methods
    #place symbol on game board
    def place_symbol(self, location_choice): #location choice is an integer
        
        if location_choice in self.valid_coord_choices:           #if location_choice is available on tictactoe board
            row, col = self.valid_coord_choices[location_choice]  #store the row and col that corresponds with selected location 
            try: #incase if current_player has an invalid value
                current_symbol = self.symbol[self.current_player] #choose the current symbol depending on the current player
                self.game_board.board[row][col] = current_symbol  #assign the current symbol to the selected location on game board
                self.valid_coord_choices.pop(location_choice)     #when a location is used remove it as a possible valid location

                #self.check_winner() #check_winner should be handled outside of object
                return "success"     #sucessfully placed a symbol on board
            except KeyError:
                return "Invalid Player"     
        else:
            return "Invalid board location" #location_choice is an invalid value or not available
    #check current board for a winner
    def check_winner(self): 
        if self.__check_column() or self.__check_row() or self.__check_diagonal(): #check all rows,cols, diagonals for matching triplet
            self.win_status = game_state.WIN  
        elif len(self.valid_coord_choices) == 0: #if no available locations then set win_status to draw
            self.win_status = game_state.DRAW

    #private methods
    #check if a list has all same symbols
    def __list_same(self,item_list):
        if item_list[0] != 'X' and item_list[0] != 'O': #if a space has no symbol return false
            return False
        
        first_item = item_list[0] #compare the first item in list to all other items
        for index in range(1,self.game_board.BOARD_DIMENSION): 
            if (item_list[index] != 'X' and item_list[index] != 'O') or first_item != item_list[index]: #check if other indexes have no symbol or do not match first item
                return False
        return True
    
    #check all cols for a match
    def __check_column(self):
        for i in range(self.game_board.BOARD_DIMENSION):     #iterate thru e/ column
            col_list = [c[i] for c in self.game_board.board] #store one col in col_list
            if self.__list_same(col_list):  
                return True
        
        return False

    #check all rows for match
    def __check_row(self):
        for row in self.game_board.board: #iterate thru e/ ro
            if self.__list_same(row):     #row is a single row from board
                return True
        return False
    
    #check both diagonals for match
    def __check_diagonal(self):
        diag1 = []
        for i in range(self.game_board.BOARD_DIMENSION): #iterate thru e/ item along diagonal 1
            diag1.append(self.game_board.board[i][i])    #append e/ item to diag1 string
        
        if self.__list_same(diag1):
            return True
        
        diag2 = []
        for r in range(self.game_board.BOARD_DIMENSION): #iterate thru e/ item along diagonal 2
            c = self.game_board.BOARD_DIMENSION - 1 - r  #inital value for the column index 
            diag2.append(self.game_board.board[r][c])    #append e/ item to diag2 string
                                                         #row index increases while col index decreases
        if self.__list_same(diag2):
            return True
        
        return False
