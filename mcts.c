#include "mcts.h"

#include <time.h>

int g_nsims = 0;

typedef struct _State{
	int board[10][10];
	int curr;
	int player; 
	int b_in_progress = 1;
} State;

typedef struct _MCTS{
	struct State *s; //this is the board
	int opponent; 
	float limit; //this is the time limit
} MCTS;


int state_opponent(struct State *s);
{
	return 3 - s->player;
}

Node* select_node(Node *n)
{
	while(n->children != NULL)
	{
		struct Node *children[] = n->children;
		n = children[0];
		for(int i = 0; i < sizeof(children) / sizeof(*Node); i++)
		{
			if(children[i].ucb > n.ucb)
			{
				n = children[i];
			}
		}
	}
	return n;
}
Node* expand_node(MCTS *mcts, Node *n)
{
	if(n->s->b_in_progress == 0)
	{
		return n;
	}
	int moves[] = find_legal_moves(n->s);
	int gl_opponent = state_opponent(n->s);
	int opponent    = state_opponent(mcts->s);
	for(int i = 0; i < moves; i++)
	{
		int res = make_move(moves[i], opponent, n->s);
		State *new_state = malloc(sizeof(*state));
		memcpy(new_state, n->s, sizeof(*state));

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

int find_next_move(MCTS *mcts, struct State *in_state)
{
	//create the root node

	
	struct Node *root = malloc(sizeof(*Node));
	root->s = in_state;


	clock_t start;
	start = clock();
	clock_t end;
	end = clock();
	double time_taken = 0;
	while(time_taken < 3.00)
	{
		g_nsims++;
		struct Node *node = select_node(tree);
		struct Node *next_node = expand_node(node);
		int result = run_simulation(next_node);

		back_propogation(result, next_node);

		end = clock() - start;
		time_taken = (double(t))/CLOCKS_PER_SECOND;
	}

	return best_move(root);
}