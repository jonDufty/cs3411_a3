// Search Tree ADT for MCTS Search Implemention
// Take 2 ....

// typedef struct Node * TreeNode;
typedef struct Node node;
typedef struct State state;

typedef struct MCTS mcts;

int state_opponent(state *s);

int find_next_move();

node * select_node(node *n);

node * expand_node(mcts *mcts, node *n);

int run_simulation(node *n);

void back_propogation(int result, node *n);

int best_move(node *root);

// creates an empty tree node
node* newNode();

// Creates a node from a given state
node* createNode(state *State);

// Adds a node as a child of a tree given the board
void addLeaf(node* parent, node* leaf);

// Returns ucb value for node
float ucb(node* n);


