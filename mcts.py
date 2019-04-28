#!/usr/bin/python3
#MCTS implementation by Jon Dufty and Nimrod Wynne

from datetime import datetime, timedelta
from random import random
from Board import Board
from Tree import *

class MCTS:
    def __init__(self, state, limit = 10):
        self._limit = limit
        self._state = state

    # Getter method
    @property
    def state(self):
        return self._state
    @property
    def limit(self):
        return self._limit
        
    def find_next_move(self, state):
        # create new tree
        tree = Tree(state)
        root = Tree.root

        # populate with nodes
        time = datetime.datetime
        start = time.now()
        while ((time.now() - start).seconds < self.limit):
            Node.n_sims += 1
            node = self.select_node(root)
            next_node = self.expand_node(node)
            result = self.run_simulation(next_node)
            # Update statistics for each node
            self.back_propogation(result, next_node)
        return self.best_move(root)

    # select node to expand based on UCT
    # Traverse through tree recursively until finding leaf
    def select_node(self,node):
        children = node.get_children()
        if not children:
            return None
        else:
            max_c = children[0]
            for c in children:
                if c.ucb() > max_c.ucb():
                    max_c = c
            return self.select_node(max)

    # Expands selected node to find potential moves
    def expand_node(self, node):
        # Find legal moves
        moves = node.state.find_legal_moves()
        for m in moves:
            # Create new node for each child and add to child array
            new_state = node.state.make_move(m)
            new = Node(new_state, node)
            node.add_child(new)
        return random.choice(node.children)

   
    # Run simulation for expanded node
    # Randomly select down until an end state is reached
    def run_simulation(self, node):
        # Create temporary node and state (board)
        temp_state = node.get_state()
        while temp_state.in_progress is True:
            next_move = temp_state.random_move()
            result = temp_state.make_move(next_move)
        return result


    # Back propogates through nodes to update statistic
    def back_propogation(self, result, node):
        # Back propagate through node parernts
        while node.get_parent() is not None:
            node.inc_visit()
            if(node.state.player is result):
                node.inc_win()
                node = node.get_parent()


    def best_move(self, root):
        # Pick node with best statistic
        children = root.get_children()
        if not children:
            print("No children!!!")
            return -1
        else: 
            max_child = children[0]
            for x in children:
                if x.win/x.visit > max_child.win/max_child.visit:
                    max_child = x
            return max_child

#these are nodes, that will make up the tree, this is a representation of the big board i.e. the 9x9 board
#
class Board(object):
    def __init__(self):
        self.board       
        self.curr        
        self.curr_player
    def start(self, board, current_board):
        # Returns a representation of the starting state of the game.
        self.board       = board
        self.curr        = current_board
        self.curr_player = 1

    #Agent Victory  : 1
    #Opponent Vic   : 2
    #Draw           : 3
    #Non-final state: 0
    def check_victory():
        board = self.board[self.curr]
        # empty = 0, I played = 1, they played = 2
        if board[1] == board[2] == board[3] == 1:
            return 1
        if board[1] == board[4] == board[7] == 1:
            return 1
        if board[1] == board[5] == board[9] == 1:
            return 1
        if board[2] == board[5] == board[8] == 1:
            return 1
        if board[3] == board[6] == board[9] == 1:
            return 1
        if board[3] == board[5] == board[7] == 1:
            return 1
        #check opponent positions    
        if board[4] == board[5] == board[6] == 2:
            return 2
        if board[7] == board[8] == board[9] == 2:
            return 2
        if board[1] == board[2] == board[3] == 2:
            return 2
        if board[1] == board[4] == board[7] == 2:
            return 2
        if board[1] == board[5] == board[9] == 2:
            return 2
        if board[2] == board[5] == board[8] == 2:
            return 2
        if board[3] == board[6] == board[9] == 2:
            return 2
        if board[3] == board[5] == board[7] == 2:
            return 2
        if board[4] == board[5] == board[6] == 2:
            return 2
        if board[7] == board[8] == board[9] == 2:
            return 2 
        #check draw state
        if all(x != 0 for x in board):
            return 3
        #if agent and opponent have not won, and it's not a draw, it's a non-win state
        return 0   

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        pass

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

    #returns all the current legal moves of the board
    def find_legal_moves(in_board, board_num):
        curr_board = in_board[board_num]
        curr_board = curr_board[1:]
        legal_moves = []
        i = 1
        for x in curr_board:
            if x == 0:
                legal_moves.append(i)
            i += 1
        return legal_moves

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        pass

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass

class Tree:
    def __init__(self):
        self.root = None
    def set_root(Node):
        self.root = Node
    #this function finds the max ucb value of a node's children
    def ucb(node):
        #WARNING! The ni and t have to be brought from somewhere
        wi = node.get_win()
        ni = node.get_num_sims() #number of sims in this node after the ith move
        c  = 1.414 #root 2
        t  = node.get_total_sims() #total sims after i moves, #NOTE not sure where this value comes from 
        res = (wi / ni) + (c * math.sqrt(math.log(t) / ni) )
        return res
    def max_ucb_node(node):
        #get the children of the node
        children = node.get_children()
        #apply the ucb function to the entire list
        ucb_list = children
        map(ucb, ucb_list)
        #return the max value from the child list, this gets the max ucb list elem and returns the
        #corresponding 'children' elements
        max_ucb = ucb_list[0]
        i = 0
        max_index = 0
        for x in ucb_list:
            if x > max_ucb:
                max_ucb = x
                max_index = i
            i += 1
        return children[i]


#state class contains the board, current 'subboard' and the player whose turn it is
class State:
    def __init__(self, board, curr, player):
        self.board  = board
        self.curr   = curr
        self.player = player
    def get_player():
        return self.player
    def get_board():
        return self.board
    def get_curr():
        return self.curr
    def set_board(board):
        self.board = board
    def set_curr(curr):
        self.curr = curr

class Node:
    def __init__(self, state, parent):
        self.curr_state = state #the state the node represents
        self.parent     = parent #the parent of the node (None if root)
        self.win        = 0 #number of wins at this node
        self.visit      = 0 #number of visits to this node
        self.num_sims   = 0 #number of simulations performed to this node
        self.children   = [] #the children of this node
        self.status     = "IN_PROGRESS" #In progress by default, should make an enum for this

    #select a random move from this node
    def random_move():
        n = np.random.randint(1,9)
        board = self.curr_state.get_board()
        curr = self.curr_state.get_curr()
        while board[curr][n] != 0:
            n = np.random.randint(1,9)
        return n

    #update the positions on the board with the move
    def make_move(move):
        self.curr_state.set_board(move.get_board())
        self.curr_state.set_curr(move.get_curr())

    #add a child to this node
    def add_child(Node):
        self.children.append(Node)

    def get_state():
        return self.curr_state      
    def get_status():
        return self.status  
    def get_children():
        return self.children
    def get_parent():
        return self.parent
    def get_visit():
        return self.visit
    def get_win():
        return self.win
    def get_num_sims():
        return self.num_sims
    def get_board():
        return self.curr_state.get_board()
    def get_curr():
        return self.curr_state.get_curr()


    #set the parent of this node to the one passed into the argument
    def set_parent(Node):
        self.parent = Node
    def set_win(win):
        self.win = win
    def set_visit(visit):
        self.visit = visit

    #incrementor functions
    def inc_sims():
        self.num_sims += 1
    def inc_win(win):
        self.win += win
    def inc_visit(visit):
        self.visit += visit
