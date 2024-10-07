# Ship placement computer with functions at fixed positions

def ship_placement_computer(board_10x10_computer, ship_positions):

    for (r, c) in ship_positions:
            board_10x10_computer [r][c] = 'S'  # 'S' represents the ship

# Ships:

size_of_ships = {'ship1': 1,
         'ship2': 2,
         'ship3': 3,
         'ship4': 4,
         }

number_of_ships = {'ship1': 4,
         'ship2': 3,
         'ship3': 2,
         'ship4': 1,
         }

ship_positions = [
    [(0, 0)], [(0, 2)], [(0, 4)], [(0, 6)],  # Single-position ships
    [(3, 1), (3, 2)], [(3, 4), (3, 5)], [(3, 7), (3, 8)],  # Two-position ships
    [(4, 6), (5, 6), (6, 6)],  # Three-position ship
    [(6, 0), (7, 0), (8, 0)],  # Another three-position ship
    [(6, 9), (7, 9), (8, 9), (9, 9)]  # Four-position ship
]

# Place the ships on the board
for ship in ship_positions:
    ship_placement_computer(board_10x10_computer, ship)

# Example of what the board (10x10) would look like
import pprint
pprint.pprint(board_10x10_computer)


# Ship placement user with functions at fixed positions

def ship_placement_user(board_10x10_user, ship_positions):

    for (r, c) in ship_positions:
            board_10x10_user [r][c] = 'S'  # 'S' represents the ship

# Ships:

size_of_ships = {'ship1': 1,
         'ship2': 2,
         'ship3': 3,
         'ship4': 4,
         }

number_of_ships = {'ship1': 4,
         'ship2': 3,
         'ship3': 2,
         'ship4': 1,
         }

ship_positions = [
    [(1, 0)], [(1, 2)], [(1, 4)], [(1, 6)],  # Single-position ships
    [(9, 1), (9, 2)], [(9, 4), (9, 5)], [(9, 7), (9, 8)],  # Two-position ships
    [(4, 6), (5, 6), (6, 6)],  # Three-position ship
    [(5, 1), (6, 1), (7, 1)],  # Another three-position ship
    [(0, 9), (1, 9), (2, 9), (3, 9)]  # Four-position ship
]

# Place the ships on the board
for ship in ship_positions:
    ship_placement_computer(board_10x10_user, ship)

# Example of what the board (10x10) would look like
import pprint
pprint.pprint(board_10x10_user)