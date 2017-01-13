#!/usr/bin/python3
import minmax
import os
import datetime
import time
import random
import copy 
from params import *

def get_alice(win=None, filename=None):
	if filename==None:
		filename=const_db
	init_db=False
	if not(os.path.exists(filename)):
		init_db=True
	alice=minmax.AI(filename) 
	alice.try_new_stuff=True #otherwise cannot play against human
	if init_db:
		alice.init_db() 
	alice.init_state(win, [], False)
	alice.init_state(win, [], True) 
	alice.init_points(win, -1, False) # it's bad if the win value is reach and it's my turn to play
	alice.init_points(win, 1, True) # it's good if the win value is reached and it's the other turn's to play 
	return alice

def one_game(alice=None, verbose=0, init=[], learning=True, win=None, list_actions=None): 
	if win==None:
		win=const_win
	if list_actions==None:
		list_actions=const_actions
	if alice==None:
		alice=get_alice(win)
	alice.verbose=verbose>1
	state=0
	states=[]
	init=copy.copy(init)
	opponent=False
	no_end_loop=False
	while (state < win) and (not no_end_loop):
		states.append(state)  #?
		actions=[a for a in list_actions if a+state<=win]
		if (len(actions)==0):
			no_end_loop=True
		else:
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
			opponent=not opponent
	states.append(win) 
	alice.verbose=verbose>2
	if learning:
		for i in range(win,-1,-1):
			alice.calculate(i, False)
			alice.calculate(i, True) 
	if no_end_loop:
		alice.init_points(state, -1, False) # it's bad if the win value is reach and it's my turn to play
		alice.init_points(state, -1, True) # it's bad for the other too, just avoid 
	return states, opponent

def multiple_games(cpt=1000, alice=None, init=[], log=False, win=None, list_actions=None):
	a=datetime.datetime.now()
	if win==None:
		win=const_win
	if list_actions==None:
		list_actions=const_actions
	if alice==None:
		alice=get_alice(win, filename=':memory:')
	p=-1
	if log:
		log=open('log_%s' % time.strftime("%Y-%m-%d_%H-%M-%S", datetime.datetime.now().timetuple()), 'w')
	old_game=[]
	done=True
	for i in range(cpt+1):
		oldp=p
		p=int(i/cpt*100)
		if oldp!=p:
			print("\033[0G%d %%" % p, end="", flush=True) 
		game=one_game(alice=alice, verbose=0, init=init, win=win, list_actions=list_actions) 
		if log:
			log.write('%s\n' % str(game)) 
		if game==old_game:
			done=True
			break
		old_game=game
	alice.dump_to_disk(const_db)
	b=datetime.datetime.now() 
	c=b-a 
	if done:
		print("\033[0K\033[0Gdone in %d iterations in %d secondes" % (i, c.total_seconds()))
	else:
		print("\033[0K\033[0Gnot done in %d iterations in %d secondes" % (i, c.total_seconds()))
	if log:
		game=one_game(verbose=0, win=win, list_actions=list_actions)
		log.write("final : %s\n" % str(game)) 
	
	return done

