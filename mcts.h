/*********************************************************
 *  mcts.h
 *  Nine-Board Tic-Tac-Toe Agent
 *  COMP3411/9414/9814 Artificial Intelligence
 */

#include "Tree.h"

#include "Tree.h"

typedef struct State State;
typedef struct MCTS MCTS;

int state_opponent(struct State *s);

int find_next_move();

Node * select_node(Node *n);

Node * expand_node(MCTS *mcts, Node *n);

int run_simulation(Node *n);

void back_propogation(int result, Node *n);

int best_move(Node *root);