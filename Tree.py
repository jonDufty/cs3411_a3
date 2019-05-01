#!/usr/bin/python3
from Board import Board
import math
import copy

'''
Node class represents individual states in search tree for MCTS
These are used to traverse through different state possibilities, and record
statisitcs for each move
'''
class Node():

    #Class variable to keep track of total simulations in the tree 
    n_sims = 0 
    
    def __init__(self, state, move, level=0, parent=None):
        self._state = state         #the state (class) the node represents
        self._parent     = parent   #the parent of the node (None if root)
        self._win        = 0        #number of wins at this node
        self._visit      = 0        #number of visits to this node
        self._children   = []       #the children of this node (i.e. possible moves)
        self._move       = move     #the move taken to get to this state
        self.level       = level    #The depth of the tree at this point, used for debugging mainly
    

    #add a child to this node
    def add_child(self, node):
        self._children.append(node)

    # Reset sim count for new tree
    def reset_sims(self):
        Node.n_sims = 0

    
    #Finds the max Upper Confidence Bound (UCB) value of a node's children
    # To give an indication of which node to picj next
    def ucb(self):
        w = float(self.win)
        n = float(self.visit)  
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
    @property
    def player(self):
        return self._state.player

    #incrementor functions
    def inc_sims(self):
        Node.n_sims += 1
    def inc_win(self,w=1):
        self._win += w
    def inc_visit(self):
        self._visit += 1

'''
Tree Class used to track root of tree and reset total simulation count each time a new tree is created
'''
class Tree(object):
    def __init__(self, root):
        self._root = root       #set the root as an argument for the class
        self.root.reset_sims()  #Called when initialised to reset the class variable in Node

    @property
    def root(self):
        return self._root