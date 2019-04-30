// Search Tree ADT for MCTS Search Implemention
// Take 2 ....
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <math.h>
#include "Tree.h"


int g_nsims = 0;

typedef struct MCTS{
	state *state; //this is the board
	int opponent; 
	float limit; //this is the time limit
} mcts;

typedef struct Node {
    struct State *state;
    struct Node *parent;
    int win;
    int visit;
    struct Node **children;
} node;

typedef struct State{
    int board[10][10];
    int curr;
    int player; 
    int b_in_progress;
} state;

int n_sims = 0;

// creates an empty tree node
node* newNode()
{
    node* n;
    n = malloc(sizeof(node));
    assert (n != NULL);
    n->win = 0;
    n->visit = 0;
    n->parent = NULL;
    n->children = calloc(9,sizeof(node));
    n->state = NULL;
    return n;
}

//Creates node given state info 
node* createNode(state *state)
{
    node* new = newNode();
    memcpy(new->state, state, sizeof(state));
    return new;
}


// Adds a node as a child of a tree
void addLeaf(node* parent, node* child)
{
    // Add child to parent
    if(parent == NULL) return;
    int i;
    while(parent->children[i] != NULL){
        i++;
    }
    parent->children[i] = child;

    // Add parent pointer to child
    if (child != NULL){
        child->parent = parent;
    }
    return;    
}

// Returns ucb value for node
float ucb(node* t)
{
    float ucb = (float)(((float)t->win/(float)t->visit) + sqrt(log(n_sims)/(double)t->visit));
    return ucb;
}

int state_opponent(state *s)
{
	return 3 - (s->player);
}

node* select_node(node *n)
{
	while(n->children[0] != NULL)
	{
		node **children = n->children;
		n = children[0];
		for(int i = 0; i < sizeof(children) / sizeof(node*); i++)
		{
			if(ucb(children[i]) > ucb(n))
			{
				n = children[i];
			}
		}
	}
	return n;
}

int run_simulation(node *n)
{
	//run the simulation on the nodes
    state *temp_state = malloc(sizeof(*state));
    int result = temp_state->player;
    while(temp_state->b_in_progress == 1)
    {
    	int next_move = random_move(temp_state);
    	result = make_move(next_move, temp_state, opponent(temp_state));
    }
    return result;
}
void back_propogation(int result, node *n)
{
	//backprop through the nodes to the parent
    node *node = n;
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

int find_next_move(mcts *mcts, struct state *in_state)
{
	//create the root node

	
	node *root = malloc(sizeof(node*));
	root->s = in_state;


	clock_t start = clock();
	clock_t end = start;

	double time_taken = 0;
	while(time_taken < 3.00)
	{
		g_nsims++;
		node *node = select_node(root);
		node *next_node = expand_node(mcts, node);
		int result = run_simulation(next_node);

		back_propogation(result, next_node);

		end = clock() - start;
		time_taken = ( (double)end )/CLOCKS_PER_SEC;
	}

	return best_move(root);
}


node* expand_node(mcts *mcts, node *n)
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
		state *new_state = malloc(sizeof(state));
		memcpy(new_state, n->state, sizeof(state));

		node* new = createNode(new_state);

		if(res == gl_opponent)
		{
            n->win = -1000;
		}
        add_leaf(n, new);
	}
	int array_size = sizeof(n->children)/sizeof(node*);
	return n->children[rand() % array_size];
}

