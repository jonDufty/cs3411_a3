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
                if x.get_visit > max_child.get_visit():
                    max_child = x
            return max_child