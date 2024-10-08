# Empty boards
board_computer = []
#launch_board_computer = []
board_user = []
launch_board_user = []

#Create a board with dimensions 'rows' x 'columns' and fill it with the value '_'
def create_board(rows, columns, fill='_'):
    
    board = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(fill)
        board.append(row)
    return board

import pprint

board_computer = create_board(board_size,board_size)
#pprint.pprint(board_computer)
#print()
#launch_board_computer = create_board(board_size,board_size)
#pprint.pprint(launch_board_computer)
#print()
board_user = create_board(board_size,board_size)
#pprint.pprint(board_user)
#print()
launch_board_user = create_board(board_size,board_size)
#pprint.pprint(launch_board_user)