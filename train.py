#!/usr/bin/python3
import minmax
import os
import datetime
import time
import random
import copy

const_win=100
const_max=10

db='/tmp/ai.db'
init_db=False
if not(os.path.exists(db)):
	init_db=True
alice=minmax.AI(db) 
alice.try_new_stuff=False
if init_db:
	alice.init_db()

alice.init_state(const_win, [], False)
alice.init_state(const_win, [], True)

alice.init_points(const_win, -1, False) # it's bad if the win value is reach and it's my turn to play
alice.init_points(const_win, 1, True) # it's good if the win value is reached and it's the other turn's to play

def one_game(verbose=0, init=[], learning=True): 
	alice.verbose=(verbose>1)
	state=0
	states=[]
	init=copy.copy(init)
	while state < const_win: 
		states.append(state)
		max_act=min(const_max, const_win-state)
		actions=list(range(1, max_act+1))
		alice.init_state(state, actions, False)
		alice.init_state(state, actions, True) # situations and what u can do with them are the samefor both players
		if len(init)>0:
			action=init.pop(0) 
		else:
			action=alice.play(state, actions)
		old_state=state
		state+=action
		alice.init_path(old_state, action, state, False)
		alice.init_path(old_state, action, state, True) # for the same score, the same action leads to the same path, for both players. That is often the case
	states.append(const_win) 
	alice.verbose=False
	if learning:
		for i in range(const_win,-1,-1):
			alice.calculate(i, False)
			alice.calculate(i, True) 
	return states

def multiple_games(cpt, init=[]):
	p=-1
	log=open('log_%s' % time.strftime("%Y-%m-%d_%H-%M-%S", datetime.datetime.now().timetuple()), 'w')
	old_game=[]
	for i in range(cpt+1):
		oldp=p
		p=int(i/cpt*100)
		if oldp!=p:
			print("\033[0G%d %%" % p, end="", flush=True) 
		game=one_game(verbose=0, init=init) 
		log.write('%s\n' % str(game)) 
		if game==old_game:
			break
		old_game=game
	print("\033[0K\033[0Gdone in %d iterations" % i)
	game=one_game(verbose=0)
	log.write("final : %s\n" % str(game))


