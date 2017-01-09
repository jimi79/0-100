#!/usr/bin/python3
import minmax
import os
import random

const_win=100
const_max=10

db='/tmp/ai.db'
init_db=False
if not(os.path.exists(db)):
	init_db=True
alice=minmax.AI(db) 
if init_db:
	alice.init_db()

alice.init_state(const_win, [], False)
alice.init_state(const_win, [], True)

alice.init_points(const_win, -1, False) # it's bad if the win value is reach and it's my turn to play
alice.init_points(const_win, 1, True) # it's good if the win value is reached and it's the other turn's to play

def one_game(verbose=True):
	alice.verbose=verbose
	state=0
	while state < const_win: 
		if verbose:
			print(state)
		max_act=min(const_max, const_win-state)
		actions=list(range(1, max_act+1))
		alice.init_state(state, actions, False)
		alice.init_state(state, actions, True) # situations and what u can do with them are the samefor both players
		action=alice.play(state, actions)
		old_state=state
		state+=action
		alice.init_path(old_state, action, state, False)
		alice.init_path(old_state, action, state, True) # for the same score, the same action leads to the same path, for both players. That is often the case

	alice.verbose=False
	#alice.recurse_calculate(const_win, False) # too long goddamnit
	#alice.recurse_calculate(const_win, True)
	for i in range(const_win,-1,-1):
		alice.calculate(i, False)
		alice.calculate(i, True)

def multiple_games(cpt):
	p=-1
	for i in range(cpt):
		oldp=p
		p=int(i/cpt*100)
		if oldp!=p:
			print("\033[0G%d %%" % p, end="", flush=True) 
		one_game(verbose=False) 
		if alice.is_over():
			break
	print("\033[0K\033[0Gdone")
