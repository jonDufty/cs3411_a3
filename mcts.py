#!/usr/bin/python3
#MCTS implementation by Jon Dufty and Nimrod Wynne

import random
import datetime
import copy
from Board import Board
from Tree import *

t_moves = 0

class MCTS:
    def __init__(self, state, limit = 3):
        self._limit = limit
        self._state = state
        self._move_lim = 500

    # Getter method
    @property
    def state(self):
        return self._state
    @property
    def limit(self):
        return self._limit
        
    def find_next_move(self):
        global t_moves
        t_moves += 2
        # create new tree
        root = Node(copy.deepcopy(self.state), -1)
        root.state._player = self.state.opponent()
        tree = Tree(root)
        # populate with nodes
        time = datetime.datetime
        start = time.now()
        while ((time.now() - start).seconds < self.limit):
        # while (Node.n_sims < self._move_lim):
            Node.n_sims += 1
            node = self.select_node(root)
            next_node = self.expand_node(node)
            result = self.run_simulation(next_node)
            # Update statistics for each node
            if next_node.state.in_progress is False:
                self.back_propogation(result, next_node, 10)
            self.back_propogation(result, next_node, 1)
        # if t_moves > 30:
            # tree.print_tree(root)
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
        # don't expand node if it is an end state
        if node.state.in_progress is False:
            return node
        # Find legal moves
        moves = node.state.find_legal_moves()
        # player = self.state.player
        gl_opponent = self.state.opponent()
        opponent = node.state.opponent()
        for m in moves:
            # Create new node for each child and add to child array
            new_state = copy.deepcopy(node.state)
            res = new_state.make_move2(m, opponent)
            new = Node(new_state, m, node.level+1, node)
            if res == gl_opponent:
                node._win = -100000
                node.state._in_progress = False
            node.add_child(new) 
        return random.choice(node.children)

   
    # Run simulation for expanded node
    # Randomly select down until an end state is reached
    def run_simulation(self, node):
        # Create temporary node and state (board)
        if node.state.in_progress is False:
            return node.state.player

        temp_state = copy.deepcopy(node.state)
        result = 0
        # i = 0
        while temp_state.in_progress is True:
            next_move = temp_state.random_move()
            result = temp_state.make_move2(next_move, temp_state.opponent())
            # i += 1
        return result


    # Back propogates through nodes to update statistic
    def back_propogation(self, result, node, inc):
        # Back propagate through node parernts
        while node.parent is not None:
            node.inc_visit()
            if(node.state.player is result):
                node.inc_win(inc)
            node = node.parent
        node.inc_visit()

    def best_move(self, root):
        global t_moves
        # Pick node with best statistic
        children = root.children
        print("\n")
        if not children:
            print("No children!!!")
            return -1
        else: 
            max_child = children[0]
            for x in children:
                x.print_state()
                if x.win/x.visit > max_child.win/max_child.visit:
                    max_child = x
            # print(root.board[root.curr])
            # print(root.board)
            print("legal moves = ", root.state.find_legal_moves())
            print("best move = ",max_child.move)
            print(Node.n_sims)
            return max_child.move



"""

./servt -p 12345 &
./agent.py -p 12345 &
./randt -p 12345

"""

# if __name__ == "__main__":
#     import numpy as np
#     import random
#     # the boards are of size 10 because index 0 isn't used
#     boards = np.zeros((10, 10), dtype="int8")
#     s = [".","X","O"]
#     curr = 1 # this is the current board to play in

#     # Create global board object
#     g_board = Board(boards,curr)
#     print(g_board.board)
#     test = MCTS(g_board)
#     n = test.find_next_move()
#     print(n)