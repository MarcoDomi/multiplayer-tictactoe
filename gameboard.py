
class tictactoe_board:
    def __init__(self):
        self.board = [[1,2,3], [4,5,6], [7,8,9]]
        self.floor = '{:-^15}'.format('')
        self.wall = '{:^5}'.format('|') 
        self.BOARD_DIMENSION = 3

    def print_board(self): #NOTE might make this a tictatoe method
        for i in range(self.BOARD_DIMENSION): #NOTE might change so it returns a string that has board configuration
            print(f"{self.board[i][0]}{self.wall}{self.board[i][1]}{self.wall}{self.board[i][2]}")
            if i != self.BOARD_DIMENSION - 1:
                print(self.floor)

    

class tictactoe_game:
    def __init__(self):
        self.game_board = tictactoe_board()
        self.symbol = {'P1':'X', 'P2':'O'}
        self. win_status = False
        self.valid_coord_choices = {1:(0,0), 2:(0,1), 3:(0,2), #all valid locations on game board
                                    4:(1,0), 5:(1,1), 6:(1,2),
                                    7:(2,0), 8:(2,1), 9:(2,2)}
        #NOTE might add a player attribute
        #NOTE might make current_player an enum type

    def place_symbol(self, current_player, location_choice):
        
        if location_choice in self.valid_coord_choices:
            row, col = self.valid_coord_choices[location_choice] #store the row and col that corresponds with selected location 
            try: #incase if current_player has an invalid value
                current_symbol = self.symbol[current_player]     #choose the current symbol depending on the current player
                self.game_board.board[row][col] = current_symbol #assign the current symbol to the selected location on game board
                self.valid_coord_choices.pop(location_choice)    #when a location is used remove it as a possible valid location

                self.check_winner()
            except KeyError:
                print("Invalid Player") #NOTE may change to return string 

        else:
            print("Invalid board location") #NOTE might change so it returns this string

    def list_same(self,item_list):
        #all_same = True
        if item_list[0] != 'X' and item_list[0] != 'O':
            return False
        
        first_time = item_list[0]
        for index in range(1,self.game_board.BOARD_DIMENSION):
            if (item_list[index] != 'X' and item_list[index] != 'O') or first_time != item_list[index]:
                return False
        
        return True
    
    #TODO implement check col func
    #TODO implement check row func
    #TODO implement check diag func

    def check_winner(self):
        pass



t = tictactoe_game()













