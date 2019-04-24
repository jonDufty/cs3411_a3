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