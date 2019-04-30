/*********************************************************
 *  mcts.h
 *  Nine-Board Tic-Tac-Toe Agent
 *  COMP3411/9414/9814 Artificial Intelligence
 */

#include "Tree.h"


typedef struct MCTS mcts;

int state_opponent(state *s);

int find_next_move();

node * select_node(node *n);

node * expand_node(mcts *mcts, node *n);

int run_simulation(node *n);

void back_propogation(int result, node *n);

int best_move(node *root);