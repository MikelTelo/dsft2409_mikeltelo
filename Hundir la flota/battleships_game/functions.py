#!/usr/bin/env python
# coding: utf-8

# In[6]:


# functions.py

import random

from variables import board_size, size_of_ships, number_of_ships

# Function to create an empty board with 'rows' x 'columns' filled with '_'
def create_board(rows, columns, fill='_'):
    return [[fill for _ in range(columns)] for _ in range(rows)]

# Function to check if a ship can be placed at a specific position
def can_place_ship(board, ship_length, start_row, start_col, orientation):
    if orientation == 'H':
        if start_col + ship_length > board_size:
            return False
        for c in range(start_col, start_col + ship_length):
            if board[start_row][c] == 'S':
                return False
    elif orientation == 'V':
        if start_row + ship_length > board_size:
            return False
        for r in range(start_row, start_row + ship_length):
            if board[r][start_col] == 'S':
                return False
    return True


# Function to place ships randomly on the board
def place_ships_randomly(board, size_of_ships, number_of_ships):
    for ship_name, ship_length in size_of_ships.items():
        for _ in range(number_of_ships[ship_name]):
            placed = False
            while not placed:
                start_row = random.randint(0, board_size - 1)
                start_col = random.randint(0, board_size - 1)
                orientation = random.choice(['H', 'V'])
                if can_place_ship(board, ship_length, start_row, start_col, orientation):
                    if orientation == 'H':
                        for c in range(start_col, start_col + ship_length):
                            board[start_row][c] = 'S'
                    elif orientation == 'V':
                        for r in range(start_row, start_row + ship_length):
                            board[r][start_col] = 'S'
                    placed = True

# Function to handle the computer's shot
def shot_computer(board_user, row, column):
    if board_user[row][column] == 'S':
        print('Computer hit at', row, column)
        board_user[row][column] = 'X'  # Mark hit as 'X'
        return True
    elif board_user[row][column] in ('X', '0'):
        print('That position is already given, try again.')
        return True
    else:
        print('Computer missed at', row, column)
        board_user[row][column] = '0'  # Mark miss as '0'
        return False

# Function to handle the user's shot
def shot_user(board_computer, launch_board_user, row, column):
    if board_computer[row][column] == 'S':
        print('User hit at', row, column)
        launch_board_user[row][column] = 'X'  # Mark hit as 'X'
        return True
    elif launch_board_user[row][column] in ('X', '0'):
        print('That position is already given, try again.')
        return True
    else:
        print('User missed at', row, column)
        launch_board_user[row][column] = '0'  # Mark miss as '0'
        return False

# Function to count the number of 'X' (hits) on the board
def count_x(board):
    return sum(row.count('X') for row in board)

# Computer turn function with random shot
def computer_turn(board_user):
    while True:
        row = random.randint(0, 9)
        column = random.randint(0, 9)
        result = shot_computer(board_user, row, column)
        if count_x(board_user) == 20:
            return True
        if not result:
            break
    return False

# Player turn function
def player_turn(board_computer, launch_board_user):
    player_wins = False
    while True:
        row = input('Introduce a row in range 0-9 (or type "exit" to quit): ')
        if row.lower() == 'exit':
            print('Exiting the game. Goodbye!')
            return 'exit'  # Return 'exit' if user types "exit"
        row = int(row)
        while row < 0 or row > 9:
            print("Row out of range. Please enter an integer between 0 and 9:")
            row = int(input('Introduce a row in range 0-9: '))
        
        column = input('Introduce a column in range 0-9 (or type "exit" to quit): ')
        if column.lower() == 'exit':
            print('Exiting the game. Goodbye!')
            return 'exit'  # Return 'exit' if user types "exit"
        column = int(column)
        while column < 0 or column > 9:
            print("Column out of range. Please enter an integer between 0 and 9:")
            column = int(input('Introduce a column in range 0-9: '))
        
        print(f'User shoots at {row}, {column}')
        result = shot_user(board_computer, launch_board_user, row, column)
        if count_x(launch_board_user) == 20:
            player_wins = True
            break
        if not result:
            print('Turn of player finished.')
            break
    return player_wins