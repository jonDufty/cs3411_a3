// Search Tree ADT for MCTS Search Implemention
// Take 2 ....

typedef struct Node *TreeNode;

// creates an empty tree node
TreeNode newNode();

// Creates a node from a given state
TreeNode createNode(State*);

// Adds a node as a child of a tree given the board
void addLeaf(TreeNode, TreeNode);

// Returns ucb value for node
float ucb(TreeNode);

