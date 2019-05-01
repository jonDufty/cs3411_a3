#!/usr/bin/python3

import random

'''
Board Class - interchangeable with state, used to represent both the global board
and this individual states in the search tree.
'''
# Board class representing actual game state
class Board(object):
    
    def __init__(self, board, current_board):
        self._board       = board           #Array reperesent board
        self._curr        = current_board   #Current sub-booard being played on
        self._player      = 1               #The player who just made that move
        self._in_progress = True            #Booloean for if the state is terminal

    # Getter Functions
    @property
    def player(self):
        return self._player
    
    @property
    def board(self):
        return self._board

    @property
    def curr(self):
        return self._curr
    
    @property
    def in_progress(self):
        return self._in_progress

    #returns all the current legal moves of the sub-board
    def find_legal_moves(self):
        curr_board = self.board[self.curr]
        legal_moves = []
        for x in range(1,len(curr_board)):
            if curr_board[x] == 0:
                legal_moves.append(x)
        return legal_moves

    
    def make_move(self, move, player):
        self._player = player
        self._board[self._curr][move] = player
        self._curr = move
        
        # check terminal states
        if self.winner(self.player):
            self._in_progress = False 
            return self.player
        elif self.full_board():
            self._in_progress = False
            return 0
        else:
            return 0

    # Takes in a move, changes board state, sets player
    # Checks for a winner/terminal state. Returns player# for win or 0 for draw/in_progress
    def make_move2(self, move, player):
        self._player = player
        c = self._curr
        self._board[self._curr][move] = player
        winner = self.winner(self.player)
        full = self.full_board()
        self._curr = move
        # check winner
        if winner:
            self._in_progress = False 
            return self.player
        elif full:
            self._in_progress = False
            return 0
        else:
            return 0

    #select a random move from this given sub-board
    def random_move(self):
        n = random.choice(self.find_legal_moves())
        return n

    # Switch player in the state
    def toggle_player(self):
        self._player = 3 - self.player

    # Return opponent for a given player
    def opponent(self):
        return (3 - self._player)

    # Returns boolean for whether the sub-board is a winning condition for player p
    def winner(self, p):
        curr = self.board[self.curr]
        return(  ( curr[1] == p and curr[2] == p and curr[3] == p )
                or( curr[4] == p and curr[5] == p and curr[6] == p )
                or( curr[7] == p and curr[8] == p and curr[9] == p )
                or( curr[1] == p and curr[4] == p and curr[7] == p )
                or( curr[2] == p and curr[5] == p and curr[8] == p )
                or( curr[3] == p and curr[6] == p and curr[9] == p )
                or( curr[1] == p and curr[5] == p and curr[9] == p )
                or( curr[3] == p and curr[5] == p and curr[7] == p ))

    # Checks if any given sub-board is full
    def full_board(self):
        cells = [i > 0 for i in self.board[self.curr]]
        return sum(cells) >= 9


    ''' Debugging Print Codes '''
    # print a row
    # This is just ported from game.c
    def print_board_row(self,board, a, b, c, i, j, k):
        s = [".","X","O"]
        print(" "+s[board[a][i]]+" "+s[board[a][j]]+" "+s[board[a][k]]+" | " \
                +s[board[b][i]]+" "+s[board[b][j]]+" "+s[board[b][k]]+" | " \
                +s[board[c][i]]+" "+s[board[c][j]]+" "+s[board[c][k]])

    # Print the entire board
    # This is just ported from game.c
    def print_board(self, board):
        self.print_board_row(board, 1,2,3,1,2,3)
        self.print_board_row(board, 1,2,3,4,5,6)
        self.print_board_row(board, 1,2,3,7,8,9)
        print(" ------+-------+------")
        self.print_board_row(board, 4,5,6,1,2,3)
        self.print_board_row(board, 4,5,6,4,5,6)
        self.print_board_row(board, 4,5,6,7,8,9)
        print(" ------+-------+------")
        self.print_board_row(board, 7,8,9,1,2,3)
        self.print_board_row(board, 7,8,9,4,5,6)
        self.print_board_row(board, 7,8,9,7,8,9)
        print()
