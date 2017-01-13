#!/usr/bin/python3
#todo

import minmax 
from params import * 

def play(win, list_actions, start=True, replay=False):
	first=True
	while replay or first:
		first=False
		print("First to reach %d wins" % win)
		alice=minmax.AI(const_db)
		state=0
		if start:
			action=alice.play(state, list_actions)
			print("I play %d" % action)
			state=action
		while state < win:
			actions=[a for a in list_actions if a+state<=win]
			val=int(input("Score is %d, enter value, amongst %s : " % (state, actions)))
			state+=val
			if state==win:
				print("Score is %d, you win" % win)
			else: 
				actions=[a for a in list_actions if a+state<=win]
				action=alice.play(state, actions)
				print("Socre is %d, I play %d" % (state, action))
				state+=action
				if state==win:
					print("Score is %s, I win" % win)
		s=input("Do you want to replay ? y/n ")
		if s.lower()=='n':
			replay=False

