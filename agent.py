#!/usr/bin/python3
# Sample starter code by Zac Partridge - z.partridge@unsw.edu.au
# 06/04/19
# Agent Adaption by Jonathan Dufty and Nimrod Wynne

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
#g_board is the global board class object. Curr is the current cub-board
curr = 0
g_board = Board(boards, curr)

# choose a move to play
def play():
    # Create copy of global board to pass into MCTS function
    #  (so to not update global board when simulating)
    board_copy = copy.deepcopy(g_board)
    mcts = MCTS(board_copy)
    n = mcts.find_next_move()
    
    place(curr, n, 1)
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
