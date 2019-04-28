#!/usr/bin/python3
# Sample starter bot by Zac Partridge
# Contact me at z.partridge@unsw.edu.au
# 06/04/19
# Feel free to use this and modify it however you wish

import socket
import sys
import numpy as np

import copy
from mcts import MCTS
from Board import Board

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
s = [".","X","O"]
curr = 0 # this is the current board to play in

#g_board is the global board class object
g_board = Board(boards, curr)

# print a row
# This is just ported from game.c
def print_board_row(board, a, b, c, i, j, k):
    print(" "+s[board[a][i]]+" "+s[board[a][j]]+" "+s[board[a][k]]+" | " \
             +s[board[b][i]]+" "+s[board[b][j]]+" "+s[board[b][k]]+" | " \
             +s[board[c][i]]+" "+s[board[c][j]]+" "+s[board[c][k]])

# Print the entire board
# This is just ported from game.c
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()


# #is board state a winnning position
# def is_board_state_win(player, board):
#     print("on board ", board)
#     curr_board = [1,1,1,0,0,0,0,0,0]
#     if curr_board[1] == player and curr_board[2] == player and curr_board[3] == player:
#         return player
#     if curr_board[1] == player and curr_board[4] == player and curr_board[7] == player:
#         return player
#     if curr_board[1] == player and curr_board[5] == player and curr_board[9] == player:
#         return player
#     if curr_board[3] == player and curr_board[6] == player and curr_board[9] == player:
#         return player
#     if curr_board[4] == player and curr_board[5] == player and curr_board[6] == player:
#         return player
#     if curr_board[7] == player and curr_board[8] == player and curr_board[9] == player:
#         return player
#     elif len(find_legal_moves()) > 0:
#         #continue playing
#         return 3
#     else: 
#         #draw
#         return 0



# choose a move to play
def play():
    #print_board(boards)
    # just play a random move for now
    # n = np.random.randint(1,9)
    # while boards[curr][n] != 0:
    #     n = np.random.randint(1,9)
    board_copy = copy.deepcopy(g_board)
    print_board(board_copy.board)
    mcts = MCTS(board_copy)
    n = mcts.find_next_move()
    print("Best move found: ", n)
    
    place(curr, n, 1)
    print_board(g_board.board)
    return n

# place a move in the global boards
def place(board, num, player):
    global curr
    global g_board
    curr = num
    g_board._curr = num
    g_board.board[board][num] = player

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == "third_move":
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        return play()
    elif command == "next_move":
        place(curr, int(args[0]), 2)
        return play()
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
