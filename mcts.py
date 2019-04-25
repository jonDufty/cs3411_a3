#MCTS implementation by Jon Dufty and Nimrod Wynne

import datetime 

class MonteCarlo:
    def __init__(self):
        pass

    def find_next_move(self, state):
        # create new tree
        tree = Tree(State)
        root = Tree.root
        # populate with nodes
        while (time < limit):
            node = select_node(root)
            next_node = expand_node(tree, node)
            result = run_simulation(tree, next_node)
            # Update statistics for each node
            back_propogation(next_node, result)
        return best_move(root)

    # select node to expand based on UCT
    # Traverse through tree recursively until finding leaf
    def select_node(self):
        if (node.children is None):
            return self
        else:
            #Question? Is this the same process that happens in next_state on line 119/120??
            # A: Similar for the select node part, but the part in next_state checks if there are legal moves, this checks if the node has been expanded yet
            node = tree.max_ucb_node(node)
            return select_node(node)

    # Expands selected node to find potential moves
    def expand_node(self, node):
        # Find legal moves
        moves = find_legal_moves(node.get_state())
        for m in moves:
            # Create new node for each child and add to child array
            new = Node(self, state, parent=node)
            node.add_child(new)
        return random(moves)


    # Run simulation for expanded node
    # Randomly select down until an end state is reached
    def run_simulation(self, node):
        # Create temporary node and state (board)
        temp_state = node.state
        while(tem_state.status.IN_PROGRESS):
            next_move = temp_state.random_move()
            temp_state.make_move(next_move)
        return temp_state
        #Question? Rewriting the above code with the written functions/structure, does it make sense?
        # A: Happy with that
        temp_state = node.get_state()
        while temp_state.get_status() == "IN_PROGRESS":
            next_move = temp_state.random_move()
            temp_state.make_move(next_move)
        return temp_state

    def back_propogation(self, result, node):
        # Back propagate through node parernts
        while node.get_parent() not None:
            #Question? what is result, is it a state or is it a node
            player = result.player
                node.get_visit() += 1
                if(node.get_state().get_player() == player):
                    node.set_win() += 1
                node = node.get_parent()


    def best_move(self, root):
        # Pick node with best statistic
        moves = root.child
        max = moves[0]
        for m in moves:
            if m.probability > max.probability:
               max = m
        return max
        #Question? should the above be replaced by this code, i think it's the same thing but with existing functions
        # A: Yep cool with that
        children = root_node.get_children()
        max_child = children[0]
        for x in children:
            if x.get_visit > max_child.get_visit():
                max_child = x

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

        children = root_node.get_children()
        max_child = children[0]
        for x in children:
            if x.get_visit > max_child.get_visit():
                max_child = x

        winnerNode = max_child

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
    def __init__:
        self.root = None
    def set_root(Node):
        self.root = Node

#state class contains the board, current 'subboard' and the player whose turn it is
def State:
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
        self.curr_state = state
        self.parent     = parent
        self.win        = 0
        self.visit      = 0
        self.children   = []
        self.status     = "IN_PROGRESS" #In progress by default, should make an enum for this

    #select a random move from this node
    def random_move():
        n = np.random.randint(1,9)
        while self.board[self.curr][n] != 0:
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
        return self.state      
    def get_status():
        return self.status  
    def get_children():
        return self.children
    def get_parent():
        return self.parent
    def get_visit():
        return self.visit
    def get_board():
        return self.board
    def get_curr():
        return self.curr

    #set the parent of this node to the one passed into the argument
    def set_parent(Node):
        self.parent = Node
    def set_win(win):
        self.win = win
    def set_visit(visit):
        self.visit = visit

    def inc_win(win):
        self.win += win
    def inc_visit(visit):
        self.visit += visit
