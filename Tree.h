// Search Tree ADT for MCTS Search Implemention
// Take 2 ....
#include "mcts.h"

typedef struct Node * TreeNode;
typedef struct Node Node;
typedef struct State State;
// creates an empty tree node
TreeNode newNode();

// Creates a node from a given state
TreeNode createNode(State *State);

// Adds a node as a child of a tree given the board
void addLeaf(TreeNode, TreeNode);

// Returns ucb value for node
float ucb(TreeNode);

