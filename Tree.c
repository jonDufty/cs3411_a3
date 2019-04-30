// Search Tree ADT for MCTS Search Implemention
// Take 2 ....
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <math.h>
#include "Tree.h"
#include "common.h"


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
    int num_children;
} node;

typedef struct State{
    int board[10][10];
    int curr;
    int player; 
    int b_in_progress;
} state;

int n_sims = 0;

// creates an empty tree node
mcts* new_mcts(state *s, float lim){
	mcts *m = malloc(sizeof(mcts));

	memcpy(m->state, s, sizeof(state));
	m->limit = lim;

	return m;
}

state* new_state(int board[10][10], int curr, int player)
{
	state *s = malloc(sizeof(state));

	memcpy(s->board, board, sizeof(int)*10*10);
	s->curr = curr;
	s->player = player;
	s->b_in_progress = 1;

	return s;
}

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
    n->num_children = 0;
    return n;
}

//Creates node given state info 
node* createNode(state *s)
{
    node* new = newNode();
    memcpy(new->state, s, sizeof(state));
    return new;
}


// Adds a node as a child of a tree
void addLeaf(node* parent, node* child)
{
    // Add child to parent
    if(parent == NULL) return;
    int i = 0;
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
	printf("select node||\n");
	while(n->children[0] != NULL)
	{
		node **children = n->children;
		n = children[0];
		int num_children = n->num_children;
		for(int i = 0; i < num_children; i++)
		{
			if(ucb(children[i]) > ucb(n))
			{
				n = children[i];
			}
		}
	}
	printf("end of select node||\n");
	return n;
}

int run_simulation(node *n)
{
	//run the simulation on the nodes
	printf("run sim||\n");
    state *temp_state = malloc(sizeof(state));
    int result = temp_state->player;
    while(temp_state->b_in_progress == 1)
    {
    	int num_moves = 0;
		int *moves = find_legal_moves(temp_state->board[temp_state->curr], &num_moves);
    	int next_move = random_move(moves, num_moves);
    	result = user_make_move(temp_state, next_move, state_opponent(temp_state));
    }
    printf("endof run sim||\n");
    return result;
}
void back_propogation(int result, node *n)
{
	//backprop through the nodes to the parent
	printf("backprop||\n");
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
    printf("end backprop||\n");
}

int find_next_move(mcts *mcts, state *in_state)
{
	//create the root node
	printf("Finding Next Move||\n");
	node *root = malloc(sizeof(node*));
	root->state = in_state;

	// node *next_node = NULL;

	clock_t start = clock();
	clock_t end = start;

	double time_taken = 0;
	while(time_taken < 3.00)
	{
		printf("while loop||\n");
		g_nsims++;
		node *n = select_node(root);
		node *next_node = expand_node(mcts, n);
		int result = run_simulation(next_node);

		back_propogation(result, next_node);

		end = clock() - start;
		time_taken = ( (double)end )/CLOCKS_PER_SEC;
	}

	return 8; //best_move(root);
}


node* expand_node(mcts *mcts, node *n)
{
	if(n->state->b_in_progress == 0)
	{
		return n;
	}
	int len = 0;
	int *moves = find_legal_moves(n->state->board[n->state->curr], &len);
	int gl_opponent = state_opponent(n->state);
	int opponent    = state_opponent(mcts->state);
	
	for(int i = 0; i < len; i++)
	{
		int res = user_make_move(n->state, moves[i], opponent);
		state *new_state = malloc(sizeof(state));
		memcpy(new_state, n->state, sizeof(state));

		node* new = createNode(new_state);

		if(res == gl_opponent)
		{
            n->win = -1000;
		}
        addLeaf(n, new);
	}
	printf("choosing random child||\n");
	return n->children[rand() % n->num_children];
}

int user_make_move(state *s, int move, int p)
{
	// Modify state board
	int c = s->curr;
	s->board[c][move] = p;
	s->player = p;

	int w = winner(p, s->board[c]);
	int f = fullboard(s->board[c]);
	// Update player/curr
	s->curr = move;
	// Check Winner Status
	if (w){
		s->b_in_progress = 0;
		return p;
	} else if (f){
		s->b_in_progress = 0;
		return 0;
	} else {
		return 0;
	}
}

int winner( int p, int bb[10] )
{
  return(  ( bb[1] == p && bb[2] == p && bb[3] == p )
         ||( bb[4] == p && bb[5] == p && bb[6] == p )
         ||( bb[7] == p && bb[8] == p && bb[9] == p )
         ||( bb[1] == p && bb[4] == p && bb[7] == p )
         ||( bb[2] == p && bb[5] == p && bb[8] == p )
         ||( bb[3] == p && bb[6] == p && bb[9] == p )
         ||( bb[1] == p && bb[5] == p && bb[9] == p )
         ||( bb[3] == p && bb[5] == p && bb[7] == p ));
}

/*********************************************************
   Return TRUE if this sub-board is full
*/
int fullboard( int bb[] )
{
  int c=1;
  while( c <= 9 && bb[c] != EMPTY ) {
    c++;
  }
  return( c == 10 );
}

int* find_legal_moves(int bb[], int *size)
{
	// find amount of moves
	int i =0;
	int c = 0;
	for (i = 1; i < 10; i++){
		if (bb[i] ==0) c++;
	}
	*size = c;
	int *legal = malloc(sizeof(int)*c);
	c = 0;
	for (i=1; i<10; i++){
		if (bb[i] == 0) {
			legal[c] = i;
			c++;
		}
	}
	return legal;
}

int random_move(int *moves, int size){
	int len = size;
	int i = rand() % len;
	return moves[i];
}

