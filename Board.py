#!/usr/bin/python3

import random
# Board class representing actual game state
class Board(object):
    
    def __init__(self, board, current_board):
        # Returns a representation of the starting state of the game.
        self._board       = board
        self._curr        = current_board
        self._player      = 1
        self._in_progress = True

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

    ''' Don't think we need this 
    
    def next_state(self, state, play):
        opponent = 3 - current_player()
        #root node has no parent
        root_node = Node(board, curr, None)
        tree = Tree()
        tree.set_root(root_node)

        #Question? Is this in the wrong place, it looks like you added it above (talking about the code block below)
        # A: Yes I think it should be in the MCTS class because thats the part thats actually times
        # while time is less than t seconds:
        #     selectRootNode
        #     ExpandFurther
        #     if len(find_legal_moves(self.board, self.curr)) > 0:
        #         simulatePlayout
        #         Backprop dat child

        # children = root_node.get_children()
        # max_child = children[0]
        # for x in children:
        #     if x.get_visit > max_child.get_visit():
        #         max_child = x

        # winnerNode = max_child

        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        pass
    '''
    #returns all the current legal moves of the board
    def find_legal_moves(self):
        curr_board = self.board[self.curr]
        legal_moves = []
        for x in range(1,len(curr_board)):
            if curr_board[x] == 0:
                legal_moves.append(x)
        return legal_moves

    # Takes in a move, changes board state, switches player
    # Checks for a winner
    def make_move(self, move, player):
        # print("move = ",move)
        self._player = player
        self._board[self._curr][move] = player
        self._curr = move
        # check winner
        if self.winner(self.player):
            # print(f"Player {self.player} wins!")
            self._in_progress = False 
            return self.player
        elif self.full_board():
            # print("Full Board!")
            self._in_progress = False
            return 0
        else:
            return 0

    def make_move2(self, move, player):
        # print("move = ",move)
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

    #select a random move from this node
    def random_move(self):
        n = random.choice(self.find_legal_moves())
        return n

    def toggle_player(self):
        self._player = 3 - self.player

    def opponent(self):
        return (3 - self._player)

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

    def full_board(self):
        cells = [i > 0 for i in self.board[self.curr]]
        return sum(cells) >= 9


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

''' Not actually sure if we need this '''
#state class contains the board, current 'subboard' and the player whose turn it is
class State:
    def __init__(self, board, curr, player):
        super().__init__()
        self._board  = board
        self._curr   = curr
        self._player = player
        self._in_progress = True
    
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
    
    def set_board(self,board):
        self._board = board
    
    def set_curr(self,curr):
        self._curr = curr