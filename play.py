#!/usr/bin/python3
#todo

import minmax

const_win=100
const_action=10

db='/tmp/ai.db'
alice=minmax.AI(db) 
score=1
start=False
if start:
	action=alice.play(score, list(range(10)))
	print("I play %d" % action)
	score=action
while score < 100:
	val=int(input("Score is %d, enter value : " % score))
	score+=val
	if score==100:
		print("Score is, you win")
	else: 
		actions=min(const_action, const_win - score)
		action=alice.play(score, list(range(1, actions + 1)))
		print("I play %d" % action)
		score+=action
		if score==100:
			print("Score is 100, I win")


