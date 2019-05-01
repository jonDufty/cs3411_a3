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
	// struct Node **children;
    struct Node *children[9];
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
	mcts *m = (mcts*)malloc(sizeof(mcts));
	printf("empty pointer\n");
	m->state = s;
	// memcpy(m->state, s, sizeof(state));
	m->limit = lim;
	printf("why didn't this segfault\n");

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
    n = (node*)malloc(sizeof(node));
    assert (n != NULL);
    n->win = 0;
    n->visit = 0;
    n->parent = NULL;
    // n->children = malloc(9*sizeof(node));
    n->state = NULL;
    n->num_children = 0;
    return n;
}

//Creates node given state info 
node* createNode(state *s)
{
    node* new = newNode();
    new->state = s;
    return new;
}


// Adds a node as a child of a tree
//parent child!!
void addLeaf(node* parent, node* child)
{
    // Add child to parent
    if(parent == NULL) return;
	int n_childs = parent->num_children;
    // parent->children[n_childs] = (node*)malloc(sizeof(node));
	parent->children[n_childs] = child;
	parent->num_children++;

    if (child != NULL){
        child->parent = parent;
    }
    return;    
}

// Returns ucb value for node
float ucb(node* t)
{
	if(t->visit == 0)
	{
		return 1000;
	}
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
	while(n->num_children > 0)
	{
		printf("sn while loop\n");
		//all the parent's children
		node **children = n->children;
		//get how many there are
		int num_children = n->num_children;
		printf("SELECT NODE: n has %d children\n", n->num_children);
		//select the first child
		n = children[0];
		//look for the child with the highest ubc value
		for(int i = 0; i < num_children; i++)
		{
			printf("UCB = %f\n", ucb(children[i]));
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
    state *temp_state = NULL;
	temp_state = malloc(sizeof(state));
    int temp_children = n->num_children;

	int curr = n->state->curr;
	int opponent = state_opponent(n->state);
	//for some reason the for loop corrupts the num children
	for(int j = 0; j < 10; j++)
	{
		for(int k = 1; k < 10; k++)
		{
			temp_state->board[j][k] = n->state->board[j][k];
		}
	}
	int result = temp_state->player;
	temp_state->curr  = curr;
	temp_state->player = opponent;
	temp_state->b_in_progress = n->state->b_in_progress;
	n->num_children = temp_children;
	printf("Simulating board at subboard %d, PROGRESS = %d\n", curr, temp_state->b_in_progress);


	int n_moves = 0;
    while(temp_state->b_in_progress == 1)
    {
		int array_of_ints[10];
		for(int j = 0; j < 10; j++)
		{
			if(j > 0)
			{
				int x = temp_state->board[temp_state->curr][j];
				array_of_ints[j] = x;
			}
			else{ array_of_ints[0] = 0; }
		}
		
		int *legal = NULL;
		int len = find_legal_moves(array_of_ints, legal);
		legal = malloc(sizeof(int)*len);
		int c = 0;
		for (int i=1; i<10; i++){
			if (array_of_ints[i] == EMPTY) {
				legal[c] = i;
				c++;
			}
		}
		int num_moves = 0;
    	int next_move = random_move(legal, num_moves);
    	result = user_make_move(temp_state, next_move, state_opponent(temp_state));
		n_moves++;
    }
	printf("Simulation exited after %d moves with %d\n", n_moves, result);
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

	time_t start, end;
	time(&start);
	double time_taken = 0.00;
	while(time_taken <= 2.00)
	{
		time(&end);
		time_taken = difftime(end, start);
		printf("while loop||\n");
		printf("time taken %lf\n", time_taken);
		
		g_nsims++;
		node *n = select_node(root);
		node *next_node = expand_node(mcts, n);
		int result = run_simulation(next_node);

		back_propogation(result, next_node);	
		break;	
	}
	printf("End of while loop!\n");
	return 10022;
	return 8; //best_move(root);
}


node* expand_node(mcts *mcts, node *n)
{
	printf("Beginning of expand node\n");
	if(n->state->b_in_progress == 0)
	{
		printf("TERMINAL??\n");
		return n;
	}

	int array_of_ints[10] = {};

	for(int j = 0; j < 10; j++)
	{
		// printf("j = %d\n", j);
		if(j > 0)
		{
			int x = n->state->board[n->state->curr][j];
			array_of_ints[j] = x;
		}
		else{ array_of_ints[0] = 0; }

	}
	//get the legal moves
	int *legal = NULL;
	int len = find_legal_moves(array_of_ints, legal);
	legal = malloc(sizeof(int)*len);
	int c = 0;
	for (int i=1; i<10; i++){
		if (array_of_ints[i] == EMPTY) {
			legal[c] = i;
			c++;
		}
	}



	int gl_opponent = state_opponent(n->state);
	int opponent    = state_opponent(mcts->state);
	printf("Expanding Children %d\n",len);
	
	for(int i = 0; i < len; i++)
	{
		int curr = n->state->curr;
		printf("Expanding move %d at board pos %d\n\n", legal[i], n->state->curr);
		state *new_state = NULL;
		new_state = malloc(sizeof(state));
		
		memcpy(new_state, n->state, sizeof(state));
		new_state->curr  = curr;
		new_state->player = opponent;
		new_state->b_in_progress = n->state->b_in_progress;
		if(i == 0)
		{
			n->num_children = 0;
		}
		printf("n : %d\n",n->num_children);
		int res = user_make_move(new_state, legal[i], opponent);		

		node* new = createNode(new_state);
		assert(new!= NULL);

		if(res == gl_opponent)
		{
            n->win = -1000;
		}
        addLeaf(n, new);
		
	}
	
	printf("Num childs: %d\n", n->num_children);
	int random_num = rand() % n->num_children;
	node *rand_child = n->children[random_num];
	printf("Node Chosen: %d with %d children\n", rand_child->state->curr, rand_child->num_children);
	printf("parent %p and parent %p\n", n, rand_child->parent);
	// printf("parent node: %p    rand child %p\n", n, rand_child);
	return rand_child;
}


int user_make_move(state *s, int move, int p)
{
	// Modify state board
	s->player = p;
	int c = s->curr;
	s->board[c][move] = p;
	printf("move is [%d][%d]\n", c, move);
	
	int w = winner(p, s->board[c]);
	int f = fullboard(s->board[c]);
	// Update player/curr
	s->curr = move;
	// Check Winner Status
	if (w){
		s->b_in_progress = 0;
		printf("win state!!\n");
		return p;
	} else if (f){
		s->b_in_progress = 0;
		printf("lost state!!\n");
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

int find_legal_moves(int bb[], int *legal)
{
	// find amount of moves
	int i =0;
	int c = 0;
	for (i = 1; i < 10; i++){
		if (bb[i] == EMPTY) c++;
	}
	return c;
}

int random_move(int *moves, int size){
	int len = size;
	int i = rand() % len;
	return moves[i];
}

