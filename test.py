#!/usr/bin/python3

import copy

global allgames
allgames=[]

def tree(shift='', val=0, action=0, tot=3, maxval=3, moves=[]):
	global allgames
	val+=action
	if action!=0:
		moves.append(action)
	if val==tot:
		allgames.append(moves)
	else:
		max_=min(maxval, tot-val+1)
		for i in range(1,max_):
			tree(shift=shift + '  ', val=val, action=i, tot=tot, maxval=maxval, moves=copy.copy(moves))

#r=tree(tot=100, maxval=9)

