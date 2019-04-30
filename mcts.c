#include "mcts.h"

#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <math.h>

int g_nsims = 0;


typedef struct MCTS{
	State *state; //this is the board
	int opponent; 
	float limit; //this is the time limit
} MCTS;


int state_opponent(State *s)
{
	return 3 - (s->player);
}

Node* select_node(Node *n)
{
	while(n->children[0] != NULL)
	{
		struct Node *children[] = n->children;
		n = children[0];
		for(int i = 0; i < sizeof(children) / sizeof(Node*); i++)
		{
			if(children[i]->ucb > n->ucb)
			{
				n = children[i];
			}
		}
	}
	return n;
}
Node* expand_node(MCTS *mcts, Node *n)
{
	if(n->state->b_in_progress == 0)
	{
		return n;
	}
	int moves[] = find_legal_moves(n->state);
	int gl_opponent = state_opponent(n->state);
	int opponent    = state_opponent(mcts->state);
	for(int i = 0; i < moves; i++)
	{
		int res = make_move(moves[i], opponent, n->state);
		State *new_state = malloc(sizeof(*State));
		memcpy(new_state, n->state, sizeof(*State));

		Node* new = createNode(new_state);

		if(res == gl_opponent)
		{
            n->win = -1000;
		}
        add_leaf(n, new);
	}
	int array_size = sizeof(n->children)/sizeof(*Node);
	return n->children[rand() % array_size];
}
int run_simulation(Node *n)
{
	//run the simulation on the nodes
    State *temp_state = malloc(sizeof(*State));
    int result = temp_state->player;
    while(temp_state->b_in_progress == 1)
    {
    	int next_move = random_move(temp_state);
    	result = make_move(next_move, temp_state, opponent(temp_state));
    }
    return result;
}
void back_propogation(int result, Node *n)
{
	//backprop through the nodes to the parent
    Node *node = n;
    while (node->parent != NULL)
    {
    	node->visit++;
    	if(node->state->player == result)
    	{
    		node->win++;
    	}
    	node = node->parent;
    }
    node->visit++;
}

int find_next_move(MCTS *mcts, struct State *in_state)
{
	//create the root node

	
	struct Node *root = malloc(sizeof(*Node));
	root->s = in_state;


	clock_t start = clock();
	clock_t end = start;

	double time_taken = 0;
	while(time_taken < 3.00)
	{
		g_nsims++;
		struct Node *node = select_node(tree);
		struct Node *next_node = expand_node(node);
		int result = run_simulation(next_node);

		back_propogation(result, next_node);

		end = clock() - start;
		time_taken = ( (double)end )/CLOCKS_PER_SEC;
	}

	return best_move(root);
}