// Search Tree ADT for MCTS Search Implemention
// Take 2 ....

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <math.h>
#include "Tree.h"
#include "mcts.h"


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
    Node* n;
    n = malloc(sizeof(Node));
    assert (n != NULL);
    n->win = 0;
    n->visit = 0;
    n->parent = NULL;
    n->children = calloc(9,sizeof(Node));
    n->state = NULL;
    return n;
}

//Creates node given state info 
node* createNode(State *state)
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
