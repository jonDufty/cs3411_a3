#!/usr/bin/python3
#MCTS implementation by Jon Dufty and Nimrod Wynne

import datetime
import random
import copy
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
        
    def find_next_move(self):
        # create new tree
        
        root = Node(self.state, -1)
        tree = Tree(root)

        # populate with nodes
        time = datetime.datetime
        start = time.now()
        while ((time.now() - start).seconds < self.limit):
            Node.n_sims += 1
            node = self.select_node(root)
            print("New Node Board:")
            print(node.state.board)
            next_node = self.expand_node(node)
            result = self.run_simulation(next_node)
            # Update statistics for each node
            print(f"find_next move, result = {result}")
            self.back_propogation(result, next_node)
        print("Exited while loop")
        return self.best_move(root)

    # select node to expand based on UCB
    # Traverse through tree recursively until finding leaf
    def select_node(self,node):
        children = node.children
        if not children:
            return node
        else:
            max_c = children[0]
            for c in children:
                if c.ucb() > max_c.ucb():
                    max_c = c
            return self.select_node(max_c)

    # Expands selected node to find potential moves
    def expand_node(self, node):
        # Find legal moves 
        moves = node.state.find_legal_moves()
        print(moves)
        # print(node.state.board)
        for m in moves:
            # Create new node for each child and add to child array
            new_state = copy.deepcopy(node.state)
            r = new_state.make_move(m)
            # print(vars(new_state))
            new = Node(new_state, m, node)
            node.add_child(new)
        return random.choice(node.children)

   
    # Run simulation for expanded node
    # Randomly select down until an end state is reached
    def run_simulation(self, node):
        # Create temporary node and state (board)
        # print(vars(node))
        temp_state = copy.deepcopy(node.state)
        result = 0
        while temp_state.in_progress is True:
            next_move = temp_state.random_move()
            result = temp_state.make_move(next_move)
            # print(f"run_sim - result = {result}, progress = {temp_state.in_progress}")
        # print(f"run_sim return - result = {result}")
        print(f"After END OF PLAY \n {temp_state.board} ")
        return result


    # Back propogates through nodes to update statistic
    def back_propogation(self, result, node):
        # Back propagate through node parernts
        while node.parent is not None:
            node.inc_visit()
            # print("visit= ",node.visit)
            if(node.state.player is result):
                node.inc_win()
            
            node = node.parent
        print("Exiting while loop")
            # print(vars(node))


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
            return max_child.move



"""

./servt -p 12345 &
./agent.py -p 12345 &
./randt -p 12345

"""

if __name__ == "__main__":
    import numpy as np
    import random
    # the boards are of size 10 because index 0 isn't used
    boards = np.zeros((10, 10), dtype="int8")
    s = [".","X","O"]
    curr = 0 # this is the current board to play in

    # Create global board object
    g_board = Board(boards,curr)
    print(g_board.board)
    test = MCTS(g_board)
    n = test.find_next_move()