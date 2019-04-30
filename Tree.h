// Search Tree ADT for MCTS Search Implemention
// Take 2 ....

// typedef struct Node * TreeNode;
typedef struct Node node;
typedef struct State state;
// creates an empty tree node
node* newNode();

// Creates a node from a given state
node* createNode(state *State);

// Adds a node as a child of a tree given the board
void addLeaf(node* parent, node* leaf);

// Returns ucb value for node
float ucb(node* n);

