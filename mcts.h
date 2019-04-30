/*********************************************************
 *  mcts.h
 *  Nine-Board Tic-Tac-Toe Agent
 *  COMP3411/9414/9814 Artificial Intelligence
 */





typedef struct State _State;
typedef struct MCTS _MCTS;

int state_opponent(struct state *s);

int find_next_move();

Node* select_node(Node *n);

Node* expand_node(MCTS *mcts, Node *n);

int run_simulation(Node *n);

void back_propogation(int result, Node *n);

int best_move(Node *root);