/*********************************************************
 *  agent.c
 *  Nine-Board Tic-Tac-Toe Agent
 *  COMP3411/9414/9814 Artificial Intelligence
 *  Alan Blair, CSE, UNSW
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#include "common.h"
#include "agent.h"
#include "game.h"
#include "mcts.h"
#include "Tree.h"

#define MAX_MOVE 81

int board[10][10];
int move[MAX_MOVE+1];
int player;
int m;

/*********************************************************//*
   Print usage information and exit
*/
void usage( char argv0[] )
{
  printf("Usage: %s\n",argv0);
  printf("       [-p port]\n"); // tcp port
  printf("       [-h host]\n"); // tcp host
  exit(1);
}

/*********************************************************//*
   Parse command-line arguments
*/
void agent_parse_args( int argc, char *argv[] )
{
  int i=1;
  while( i < argc ) {
    if( strcmp( argv[i], "-p" ) == 0 ) {
      if( i+1 >= argc ) {
        usage( argv[0] );
      }
      port = atoi(argv[i+1]);
      i += 2;
    }
    else if( strcmp( argv[i], "-h" ) == 0 ) {
      if( i+1 >= argc ) {
        usage( argv[0] );
      }
      host = argv[i+1];
      i += 2;
    }
    else {
      usage( argv[0] );
    }
  }
}

/*********************************************************//*
   Called at the beginning of a series of games
*/
void agent_init()
{
  struct timeval tp;

  // generate a new random seed each time
  gettimeofday( &tp, NULL );
  srandom(( unsigned int )( tp.tv_usec ));
}

/*********************************************************//*
   Called at the beginning of each game
*/
void agent_start( int this_player )
{
  reset_board( board );
  m = 0;
  move[m] = 0;
  player = this_player;
}

/*********************************************************//*
   Choose second move and return it
*/
int agent_second_move( int board_num, int prev_move )
{
  int this_move;
  move[0] = board_num;
  move[1] = prev_move;
  board[board_num][prev_move] = !player;
  m = 2;
  do {
    this_move = 1 + random()% 9;
  } while( board[prev_move][this_move] != EMPTY );
  move[m] = this_move;
  board[prev_move][this_move] = player;
  return( this_move );
}

/*********************************************************//*
   Choose third move and return it
*/
int agent_third_move(
                     int board_num,
                     int first_move,
                     int prev_move
                    )
{
  int this_move;
  move[0] = board_num;
  move[1] = first_move;
  move[2] = prev_move;
  board[board_num][first_move] =  player;
  board[first_move][prev_move] = !player;
  m=3;
  do {
    this_move = 1 + random()% 9;
  } while( board[prev_move][this_move] != EMPTY );
  move[m] = this_move;
  board[move[m-1]][this_move] = player;
  return( this_move );
}

/*********************************************************//*
   Choose next move and return it
*/
int agent_next_move( int prev_move )
{
  printf("HELALSDJASKD");
  int this_move;
  m++;
  move[m] = prev_move;
  board[move[m-1]][move[m]] = !player;
  m++;
  do {
    this_move = 1 + random()% 9;
  } while( board[prev_move][this_move] != EMPTY );
  move[m] = this_move;
  board[move[m-1]][this_move] = player;
  return( this_move );
}

/*********************************************************//*
   Receive last move and mark it on the board
*/
void agent_last_move( int prev_move )
{
  m++;
  move[m] = prev_move;
  board[move[m-1]][move[m]] = !player;
}

/*********************************************************//*
   Called after each game
*/
void agent_gameover(
                    int result,// WIN, LOSS or DRAW
                    int cause  // TRIPLE, ILLEGAL_MOVE, TIMEOUT or FULL_BOARD
                   )
{
  // nothing to do here
}

/*********************************************************//*
   Called after the series of games
*/
void agent_cleanup()
{
  // nothing to do here
}

int make_move(State *state, int move, int p)
{
	// Modify state board
	int c = state->curr;
	state->board[c][m] = p;
	state->player = p;

	w = winner(state->board[c],p);
	f = full_board(state->board[c]);
	// Update player/curr
	state->curr = move;
	// Check Winner Status
	int result = 0;
	if (w){
		state->b_in_progress = 0;
		return p;
	} else if (f){
		state->b_in_progress = 0;
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
int full_board( int bb[] )
{
  int c=1;
  while( c <= 9 && bb[c] != EMPTY ) {
    c++;
  }
  return( c == 10 );
}

int* find_legal_moves(int bb[])
{
	// find amount of moves
	int i =0;
	int c = 0;
	for (i = 1; i < 10; i++){
		if (bb[i] ==0) c++;
	}
	int *legal = malloc(sizeof(int)*c);
	c = 0
	for (i=1; i<10; i++){
		if (bb[i] == 0) {
			legal[c] = i;
			c++;
		}
	}
	return legal;
}