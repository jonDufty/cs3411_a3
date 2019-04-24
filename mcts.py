#MCTS implementation by Jon Duffy and Nimrod Wynne

class MonteCarlo:
    def __init__(self):
        pass

    # select node to expand based on UCT
    def select_node(self):
        pass

    # Expands selected node to find potential moves
    def expand_node(self):
        pass

    # Run simulation for expanded node
    def run_simulation(self):
        pass

    def get_move(self):
        move = None
        self.select_node()
        self.expand_node()
        self.run_simulation()
        # Pick node with best statistic
        return move

#these are nodes, that will make up the tree, this is a representation of the big board i.e. the 9x9 board
#
class Board(object):
    def start(self, board, current_board):
        # Returns a representation of the starting state of the game.
        self.board       = board
        self.curr        = current_board
        self.curr_player = 1
        pass

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