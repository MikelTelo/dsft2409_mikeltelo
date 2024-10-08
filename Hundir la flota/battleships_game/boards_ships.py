import random
import pprint

# Ship sizes and counts
size_of_ships = {
    'ship1': 1,  # 4 ships of size 1
    'ship2': 2,  # 3 ships of size 2
    'ship3': 3,  # 2 ships of size 3
    'ship4': 4   # 1 ship of size 4
}

number_of_ships = {
    'ship1': 4,
    'ship2': 3,
    'ship3': 2,
    'ship4': 1,
}

#ships = [1,1,1,1,2,2,2,3,3,4]

# Function to check if a ship can be placed at a specific position
def can_place_ship(board, ship_length, start_row, start_col, orientation):
    if orientation == 'H':  # Horizontal
        if start_col + ship_length > board_size:  # Check if it goes out of bounds
            return False
        for c in range(start_col, start_col + ship_length):
            if board[start_row][c] == 'S':  # Check if there's already a ship
                return False
    elif orientation == 'V':  # Vertical
        if start_row + ship_length > board_size:  # Check if it goes out of bounds
            return False
        for r in range(start_row, start_row + ship_length):
            if board[r][start_col] == 'S':  # Check if there's already a ship
                return False
    return True

# Function to place ships on the board
def place_ships_randomly(board, size_of_ships, number_of_ships):
    for ship_name, ship_length in size_of_ships.items():
        for _ in range(number_of_ships[ship_name]):
            placed = False
            while not placed:
                # Randomly select starting position and orientation
                start_row = random.randint(0, board_size - 1)
                start_col = random.randint(0, board_size - 1)
                orientation = random.choice(['H', 'V'])  # Choose horizontal or vertical

                if can_place_ship(board, ship_length, start_row, start_col, orientation):
                    # Place the ship
                    if orientation == 'H':
                        for c in range(start_col, start_col + ship_length):
                            board[start_row][c] = 'S'
                    elif orientation == 'V':
                        for r in range(start_row, start_row + ship_length):
                            board[r][start_col] = 'S'
                    placed = True  # Ship placed successfully

# Place ships randomly on the board computer-user
place_ships_randomly(board_computer, size_of_ships, number_of_ships)
place_ships_randomly(board_user, size_of_ships, number_of_ships)

#print("Computer board with ships:")
#pprint.pprint(board_computer)
#print('User outgoing board:')
#pprint.pprint(launch_board_user)
#print("User board with ships:")
#pprint.pprint(board_user)