#!/usr/bin/python3
from Board import Board
import math
from random import random

class Node():
    n_sims = 0
    def __init__(self, state, move, parent=None):
        self._state = state #the state the node represents
        self._parent     = parent #the parent of the node (None if root)
        self._win        = 0 #number of wins at this node
        self._visit      = 0 #number of visits to this node
        self._children   = [] #the children of this node
        self._move       = move
    

    #add a child to this node
    def add_child(self, node):
        self._children.append(node)

    # Reset sim count for new tree
    def reset_sims(self):
        Node.n_sims = 0

    
    #Finds the max ucb value of a node's children
    def ucb(self):
        #WARNING! The ni and t have to be brought from somewhere
        w = float(self.win)
        n = float(self.visit)    #number of sims in this node after the ith move
        if n == 0:
            return 1000
        c  = 1.414               #sqrt(2)
        t  = float(Node.n_sims)  #total sims after i moves
        # print(f"w = {w} n = {n} c = {c} t = {t}")
        res = float((w / n) + (c * math.sqrt(math.log(t) / n) ))
        return res

    # Getters and Setters
    @property
    def state(self):
        return self._state      
    @property
    def children(self):
        return self._children
    @property
    def parent(self):
        return self._parent
    @property
    def visit(self):
        return self._visit
    @property
    def win(self):
        return self._win
    @property
    def move(self):
        return self._move
    @property
    def board(self):
        return self._state.board
    @property
    def curr(self):
        return self._state.curr

    #incrementor functions
    def inc_sims(self):
        Node.n_sims += 1
    def inc_win(self):
        self._win += 1
    def inc_visit(self):
        self._visit += 1

# NOt sure if we need this at all, currently all it does it reset a count
class Tree(object):
    def __init__(self, root):
        self._root = root #set the root as an argument for the class
        self.root.reset_sims()

    @property
    def root(self):
        return self._root
'''
    def max_ucb_node(self):
        #get the children of the node
        children = self.root.get_children()
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
'''    




'''
    Previous Functions, kept just in case
    #set the parent of this node to the one passed into the argument
    # Not necessary
    def set_parent(Node):
        self._parent = Node
    def set_win(win):
        self.win = win
    def set_visit(visit):
        self._visit = visit
'''
'''
    #update the positions on the board with the move
    def make_move(self,move):
        self._state.set_board(move.get_board())
        self._state.set_curr(move.get_curr())
'''