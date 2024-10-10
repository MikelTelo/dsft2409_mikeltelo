#!/usr/bin/env python
# coding: utf-8

# In[6]:


# main_game.py

import pprint
import os
from variables import board_size, size_of_ships, number_of_ships
from functions import create_board, place_ships_randomly, player_turn, computer_turn

# Initialize the game boards
def reset_game():
    board_computer = create_board(board_size, board_size)
    board_user = create_board(board_size, board_size)
    launch_board_user = create_board(board_size, board_size)
    return board_computer, board_user, launch_board_user

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
    board_computer, board_user, launch_board_user = reset_game()
    place_ships_randomly(board_computer, size_of_ships, number_of_ships)  # Pass required arguments
    place_ships_randomly(board_user, size_of_ships, number_of_ships)  # Pass required arguments

    while True:
        player_wins = player_turn(board_computer, launch_board_user)
        os.system("cls")
        if player_wins == 'exit':
            break
        if player_wins:
            print('User wins, congratulations!!!')
            break    
        '''
        print('COMPUTER BOARD')
        pprint.pprint(launch_board_user)
        print()
        '''
        computer_wins = computer_turn(board_user)
        os.system("cls")
        if computer_wins:
            print('Computer wins, try again!!!')
            break    
        '''
        print('PLAYER BOARD')
        pprint.pprint(board_user)
        print()
        '''

# Run the menu to start the game
menu()