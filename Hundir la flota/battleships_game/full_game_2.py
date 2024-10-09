#!/usr/bin/env python
# coding: utf-8

# In[6]:


import random
import pprint

# Variables:
board_size = 10  # Board size: 10x10

# Ships:
size_of_ships = {'ship1': 1, 'ship2': 2, 'ship3': 3, 'ship4': 4}
number_of_ships = {'ship1': 4, 'ship2': 3, 'ship3': 2, 'ship4': 1}

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
def shot_computer(row, column):
    if board_user[row][column] == 'S':
        print('Computer hit at', row, column)
        board_user[row][column] = 'X'
        return True
    elif board_user[row][column] in ('X', '0'):
        print('That position is already given, try again.')
        return True
    else:
        print('Computer missed at', row, column)
        board_user[row][column] = '0'
        return False

# Function to handle the user's shot
def shot_user(row, column):
    if board_computer[row][column] == 'S':
        print('User hit at', row, column)
        launch_board_user[row][column] = 'X'
        return True
    elif launch_board_user[row][column] in ('X', '0'):
        print('That position is already given, try again.')
        return True
    else:
        print('User missed at', row, column)
        launch_board_user[row][column] = '0'
        return False

# Function to count the number of 'X' (hits) on the board
def count_x(board):
    return sum(row.count('X') for row in board)

# Computer turn function with random shot
def computer_turn():
    computer_wins = False
    while True:
        row = random.randint(0, 9)
        column = random.randint(0, 9)
        print(f'Computer shoots at {row}, {column}')
        result = shot_computer(row, column)
        if count_x(board_user) == 20:
            computer_wins = True
            break
        if not result:
            print('Turn of computer finished.')
            break
    return computer_wins

# Player turn function
def player_turn():
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
        result = shot_user(row, column)
        if count_x(launch_board_user) == 20:
            player_wins = True
            break
        if not result:
            print('Turn of player finished.')
            break
    return player_wins

# Menu for the game
def menu():
    while True:
        print("\n--- WELCOME TO BATTLESHIPS PLEASE SELECT AN OPTION FROM BELOW ---")
        print("1. Play Battleship")
        print("2. Game instructions")
        print("3. Play again")
        print("4. Exit")
        
        option = input("Select an option (1-4, or type 'exit' to quit): ")

        if option == '1':
            start_game()
        elif option == '2':
            print("\nGame Instructions:")
            print("The ships are placed randomly. You are playing against the computer. Just try to sink its ships.\n"
                  "Introduce a number between 0-9: first for a row, and second for a column. After each of your shots,\n"
                  "you'll see your shot results: 'X' for a hit, and '0' for a miss (the computer's ships are hidden).\n"
                  "Then, it's the computer's turn. You will see your board with your ships and the results of the computer's shots.\n"
                  "If you hit a ship, you can shoot again until you miss, then it's the computer's turn. The game\n"
                  "continues turn by turn until you or the computer sinks all the ships and wins. GOOD LUCK!!!")
        elif option == '3':
            print("\nStarting a new game...")
            reset_game()
            start_game()
        elif option == '4' or option.lower() == 'exit':
            print("\nThank you for playing. Goodbye!")
            break  # Break the loop to properly quit the game
        else:
            print("Invalid option. Please select an option between 1 and 4.")

# Function to start the game
def start_game():
    global board_computer, board_user, launch_board_user
    place_ships_randomly(board_computer, size_of_ships, number_of_ships)
    place_ships_randomly(board_user, size_of_ships, number_of_ships)

    while True:
        player_wins = player_turn()
        if player_wins == 'exit':  # If player chooses to exit
            break
        if player_wins:
            print('User wins, congratulations!!!')
            break    
        print('COMPUTER BOARD')
        pprint.pprint(launch_board_user)
        print()

        computer_wins = computer_turn()
        if computer_wins:
            print('Computer wins, try again!!!')
            break    
        print('PLAYER BOARD')
        pprint.pprint(board_user)
        print()

# Function to reset the game boards
def reset_game():
    global board_computer, board_user, launch_board_user
    board_computer = create_board(board_size, board_size)
    board_user = create_board(board_size, board_size)
    launch_board_user = create_board(board_size, board_size)

# Initialize the game boards
reset_game()

# Run the menu to start the game
menu()

