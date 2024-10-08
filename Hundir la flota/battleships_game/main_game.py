while True:
    player_wins = player_turn()
    if player_wins == True:
        print('User wins, congratulations!!!')
        break    
    print('COMPUTER BOARD')
    pprint.pprint(launch_board_user)
    #player_turn()
    #pprint.pprint(board_computer)
    #print("Computer board with ships hidden:")
    #print_board_hidden(board_computer)
    print()
    computer_wins = computer_turn()
    if computer_wins == True:
        print('Computer wins, try again!!!')
        break    
    print('PLAYER BOARD')
    pprint.pprint(board_user)
    print()