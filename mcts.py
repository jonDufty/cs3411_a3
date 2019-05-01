#!/usr/bin/python3
#MCTS implementation by Jon Dufty and Nimrod Wynne

import random
import datetime
import copy
from Board import Board
from Tree import *

t_moves = 0

'''
Overarching MCTS implementation and methods
Contains functions for 4 main stated of MCTS algorithm
'''
class MCTS:
    # Class Variable to track how many moves have been made to adjust time of sims
    t_moves = 0
    def __init__(self, state, limit = 3):
        self._limit = limit        #Time limits for MCTS
        self._state = state        #Initial starting state for MCTS
        self._move_lim = 500       #Move Limit for MCTS

    # Getter methods
    @property
    def state(self):
        return self._state
    @property
    def limit(self):
        return self._limit
        
    # Overarching Function, calls each step before determining optimal move
    def find_next_move(self):
        
        MCTS.t_moves += 2
        # create new tree and root node
        root = Node(copy.deepcopy(self.state), -1)
        root.state._player = self.state.opponent()
        tree = Tree(root)

        if MCTS.t_moves < 10:
            self._limit = 2
        elif MCTS.t_moves >= 10 and MCTS.t_moves< 19:
            self._limit = 4
        else:
            self._limit = 3

        # Set time limites
        time = datetime.datetime
        start = time.now()
        while ((time.now() - start).seconds < self.limit):
        # while (Node.n_sims < self._move_lim):
            # Each while loop involves 1 simulation
            Node.n_sims += 1
            # Select node based on best ucb
            node = self.select_node(root)
            # Expand node for children nodes and pick random node
            next_node = self.expand_node(node)
            # Conduct random simulation playout
            result = self.run_simulation(next_node)
            # Update statistics for each node through back prop
            if next_node.state.in_progress is False:
                # If the node is already a terminal state, back-prop has a higher weighting
                self.back_propogation(result, next_node, 10)
            self.back_propogation(result, next_node, 1)

        return self.best_move(root)

    # select node to expand based on UCB
    # Traverse through tree recursively until finding leaf
    def select_node(self,node):
        while len(node.children) > 0:
            children = node.children
            node = children[0]
            for c in children:
                if c.ucb() > node.ucb():
                    node = c
        return node

    # Expands selected node to find potential moves
    def expand_node(self, node):
        # don't expand node if it is a terminal state
        if node.state.in_progress is False:
            return node

        moves = node.state.find_legal_moves()
        global_opponent = self.state.opponent()  #Opponent for actual game
        opponent = node.state.opponent()         #Opponent with respect to the current state

        for m in moves:
            # Create new node for each child and add to child array
            new_state = copy.deepcopy(node.state)
            res = new_state.make_move2(m, opponent)
            new = Node(new_state, m, node.level+1, node)
            if res == global_opponent:
                # If the child leads to an opponent winning next move, down grade the ucb so it doesn't get picked
                node._win = -100000 
                node.state._in_progress = False
            node.add_child(new) 
        return random.choice(node.children)

   
    # Randomly simulate a game playout for expanded node
    def run_simulation(self, node):
        if node.state.in_progress is False:
            return node.state.player

        # Create temporary node and state (board)
        temp_state = copy.deepcopy(node.state)
        result = 0
        while temp_state.in_progress is True:
            next_move = temp_state.random_move()
            result = temp_state.make_move2(next_move, temp_state.opponent())
        return result


    # Back propogates through nodes to update statistic
    def back_propogation(self, result, node, inc):
        # Back propagate through node parernts
        while node.parent is not None:
            node.inc_visit()
            if(node.state.player is result):
                node.inc_win(inc)
            node = node.parent
        # Increment visits for root node
        node.inc_visit() 

    # Selects child node (from root) with best win/visit ratio
    def best_move(self, root):
        children = root.children
        if not children:
            return -1
        else: 
            max_child = children[0]
            for x in children:
                if x.win/x.visit > max_child.win/max_child.visit:
                    max_child = x
            return max_child.move
