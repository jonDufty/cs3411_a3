// Search Tree ADT for MCTS Search Implemention
// Take 2 ....

// typedef struct Node * TreeNode;
typedef struct Node node;
typedef struct State state;

typedef struct MCTS mcts;

mcts* new_mcts(state *, float);

state* new_state(int[10][10], int, int);

int state_opponent(state *s);

int find_next_move(mcts *, state *);

node * select_node(node *n);

node * expand_node(mcts *m, node *n);

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

/**  Additional State Headers  **/
int user_make_move(state*, int, int);
int winner( int p, int bb[10] );
int fullboard( int bb[] );
int* find_legal_moves(int bb[], int *size);
int random_move(int *, int size);

