
class game_board:
    def __init__(self):
        self.board = [[1,2,3], [4,5,6], [7,8,9]]
        self.floor = '{:-^15}'.format('')
        self.wall = '{:^5}'.format('|') 

    def print_board(self):
        for i in range(3):
            print(f"{self.board[i][0]}{self.wall}{self.board[i][1]}{self.wall}{self.board[i][2]}")
            if i != 2:
                print(self.floor)


class tictactoe:
    def __init__(self):
        pass


gb = game_board()
gb.print_board()
        












