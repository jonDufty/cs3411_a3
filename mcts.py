#MCTS implementation by Jon Duffy and Nimrod Wynne

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
            node = tree.max_ucb_node(node)
            return select_node(node)

    # Expands selected node to find potential moves
    def expand_node(self, node):
        # Find legal moves
        moves = get_legal_moves(node.state)
        for m in moves:
            # Create new node for each child and add to child array
            new = Node(next_state, player = opponent, parent=node)
            node.child.append(new)
        return random(moves)


    # Run simulation for expanded node
    # Randomly select down until an end state is reached
    def run_simulation(self, node):
        # Create temporary node and state
        temp_state = node.state
        while(tem_state.status.IN_PROGRESS):
            next_move = temp_state.random_move()
            temp_state.make_move(next_move)
        return temp_state

    def back_propogation(self, result, node):
        # Back propagate through node parernts
        player = result.player
        while(node.parent not None):
            node.visit += 1
            if(node.state.player == player):
                node.win += 1
            node = node.parent


    def best_move(self, root):
        # Pick node with best statistic
        moves = root.child
        max = moves[0]
        for m in moves:
            if m.probability > max.probability:
               max = m
        return max

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
        tree = new Tree() #need to create a tree class???
        establish the root node

        while time is less than t seconds:
            selectRootNode
            ExpandFurther
            check if child node has legal moves available
            simulate the playout from the child
            BACKPROPyo(child)
        winnerNode = child of root with max score()

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

class Node:
    def __init__(self, board, curr, parent):
        self.board    = board
        self.curr     = curr
        self.parent   = parent
        self.win      = 0
        self.visit    = 0
        self.children = []

    #add a child to this node
    def add_child(Node):
        self.children.append(Node)

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