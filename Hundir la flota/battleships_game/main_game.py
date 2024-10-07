import random

# Function to handle the computer's shot
def shot_computer(row, column):
    if board_10x10_user[row][column] == 'S':
        print('Computer hit at', row, column)
        board_10x10_user[row][column] = 'X'  # Mark hit as 'X'
        return True
    else:
        print('Computer missed at', row, column)
        return False
    
# Function to handle the user's shot
def shot_user(row, column):
    if board_10x10_computer[row][column] == 'S':
        print('User hit at', row, column)
        board_10x10_computer[row][column] = 'X'  # Mark hit as 'X'
        return True
    else:
        print('User missed at', row, column)
        return False

# Computer turn function with random shot
def computer_turn():
    while True:
        row = random.randint(0, 9)  # Random row between 0 and 9
        column = random.randint(0, 9)   # Random column between 0 and 9
        print(f'Computer shoots at {row}, {column}')
        result = shot_computer(row, column)  # Perform shot
        if not result:
            print('Turn of computer finished.')
            break  # End computer turn if it missed

# Player turn function
def player_turn():
    while True:
        row = int(input('Introduce a row in range 0-9: '))
        column = int(input('Introduce a column in range 0-9: '))
        print(f'User shoots at {row}, {column}')
        result = shot_user(row, column)
        if not result:
            print('Turn of player finished.')
            break

# Simulate the game by running player and computer turns alternately
while True:
    player_turn()
    pprint.pprint(board_10x10_computer)
    print()
    computer_turn()
    pprint.pprint(board_10x10_user)
    print()