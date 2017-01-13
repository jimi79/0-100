#!/usr/bin/python3

from params import *
import minmax
import os
import random
import train
import play

def generate_list():
	m=random.randrange(1,30)
	win=random.randrange(m*2,500)
	list_=list(range(1,m+1))
	for i in range(random.randrange(0, len(list_))):
		list_.pop(random.randrange(len(list_)))
	return win,list_

def train_random(win=None, list_actions=None):
	if win==None or list_actions==None:
		print("Generating a random list")
		win,list_actions=generate_list()
	if os.path.exists(db):
		os.remove(db)
	print('win = %d, actions = %s' % (win, list_actions)) 
	ok=train.multiple_games(win=win, list_actions=list_actions)
	if not ok:
		raise Exception("cannot solve")
	return win, list_actions

def stats(win, list_actions):
	if win==None:
		win,list_actions=train_()
	games=0
	opponent=0
	for i in range(11):
		stats, opponent_win=train.one_game(win=win, list_actions=list_actions)
		if opponent_win:
			opponent+=1
		games+=1
	return games, opponent
		
#win,list_=generate_list()
#train_()
#stats()
