import random

# Function to handle the computer's shot
def shot_computer(row, column):
    if board_user[row][column] == 'S':
        print('Computer hit at', row, column)
        board_user[row][column] = 'X'  # Mark hit as 'X'
        return True
    elif board_user[row][column] == 'X' or board_user[row][column] == '0':
        print('That position is alredy given, try again:')
        return True
    else:
        print('Computer missed at', row, column)
        board_user[row][column] = '0'  # Mark missed as '0'
        return False
    
# Function to handle the user's shot
def shot_user(row, column):
    if board_computer[row][column] == 'S':
        print('User hit at', row, column)
        launch_board_user[row][column] = 'X'  # Mark hit as 'X'
        return True
    elif launch_board_user[row][column] == 'X' or launch_board_user[row][column] == '0':
        print('That position is alredy given, try again:')
        return True
    else:
        print('User missed at', row, column)
        launch_board_user[row][column] = '0'  # Mark hit as '0'
        return False
    
# Function to check hits for computer and user so to end the game as soon as one of them wins the game reaching 20 hits:
def count_x(board):
    count = 0
    for row in board:
        count += row.count('X')  # Cuenta las 'X' en cada fila
    return count

count_x(launch_board_user)
count_x(board_computer)

# Computer turn function with random shot
def computer_turn():
    computer_wins = False
    while True:
        row = random.randint(0, 9)  # Random row between 0 and 9
        column = random.randint(0, 9)   # Random column between 0 and 9
        print(f'Computer shoots at {row}, {column}')
        result = shot_computer(row, column)  # Perform shot
        if count_x(board_user) == 20:
            computer_wins = True
            #print('Computer wins, try again!!!')
            break
        if not result:
            print('Turn of computer finished.')
            break  # End computer turn if it missed
    return computer_wins

# Player turn function
def player_turn():
    player_wins = False
    while True:
        #row = int(input('Introduce a row in range 0-9: '))
        #column = int(input('Introduce a column in range 0-9: '))
        row = random.randint(0, 9)  # Random row between 0 and 9
        column = random.randint(0, 9)   # Random column between 0 and 9
        print(f'User shoots at {row}, {column}')
        result = shot_user(row, column)
        if count_x(launch_board_user) == 20:
            player_wins = True
            #print('User wins, congratulations!!!')
            break
        if not result:
            print('Turn of player finished.')
            break
    return player_wins