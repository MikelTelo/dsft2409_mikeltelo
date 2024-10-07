# Empty boards
board_10x10_computer = []
outgoing_board_10x10_computer = []
board_10x10_user = []
outgoing_board_10x10_user = []

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

board_10x10_computer = create_board(board_size,board_size)
pprint.pprint(board_10x10_computer)
print()
outgoing_board_10x10_computer = create_board(board_size,board_size)
pprint.pprint(outgoing_board_10x10_computer)
print()
board_10x10_user = create_board(board_size,board_size)
pprint.pprint(board_10x10_user)
print()
outgoing_board_10x10_user = create_board(board_size,board_size)
pprint.pprint(outgoing_board_10x10_user)