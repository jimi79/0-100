#!/usr/bin/python3
#todo

import minmax 
from params import * 

alice=minmax.AI(db)
state=1
start=True
if start:
	action=alice.play(state, const_actions)
	print("I play %d" % action)
	state=action
while state < const_win:
	actions=[a for a in const_actions if a+state<=const_win]
	val=int(input("Score is %d, enter value, amongst %s : " % (state, actions)))
	state+=val
	if state==100:
		print("Score is, you win")
	else: 
		actions=[a for a in const_actions if a+state<=const_win]
		action=alice.play(state, actions)
		print("I play %d" % action)
		state+=action
		if state==const_win:
			print("Score is %s, I win" % const_win)


