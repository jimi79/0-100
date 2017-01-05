#!/usr/bin/python3

import importlib
import os
import pickle
import random
import sqlite3

#todo : 
# check we can have a status that take acocunt whos turn it is. i plan to use o0, m10, o15, m20, o23
# calculate node only if it has to be calculated. not sure how to do that. the 'parent' solution that i failed to implement should work. maybe i could try it now
# learn as it plays
# assume somethg it never tried is a good idea. with the proper distinction of status between 'me' and 'opponent', that should be easier
# would be fun to use a sqlite or any other database, instead of using memory. maybe i would actually need it, otherwise that will be slow.
# learn to turn infos into a db. the 0-100 game won't fit in memory
# if we update points, we do an sql that does only that. we don't load the object, to change the value, then save it. because that way we only save what's useful.
# 	-> define what functions are needed to handle everythg that needs to be done (init_status, init_path, calculate(status))

# i would like to find out how to calculate all possible games


class AI: 
	def __init__(self, dbname):
		self.conn=sqlite3.connect(dbname, isolation_level=None)
		self.cur=self.conn.cursor()

	def init_db(self):
		self.cur.execute('create table states(state varchar(20), points integer, minmax integer, minmax_action varchar(20), maxmin integer, maxmin_action varchar(20));')
		self.cur.execute('create unique index idx on states(state)');
		self.cur.execute('create table lt(state varchar(20), action action varchar(20), newstate varchar(20));')
		self.cur.execute('create unique index idx_lt on lt(state, action)');
		self.cur.execute('create table lto(state varchar(20), action action varchar(20), newstate varchar(20));') 
		self.cur.execute('create unique index idx_lto on lto(state, action)');

	def play(self, state): 
		# find best action with max output 
		return action

	def init_state(self, state, actions, opponent=False):
		self.cur.execute('select count(1) from states where state = ?;', (state, ))
		d=self.cur.fetchone()
		if d[0]==0: 
			self.cur.execute('begin')
			try:
				self.cur.execute('insert into states(state) values (?);', (state, ))
				if opponent:
					tablename='lto'
				else:
					tablename='lt' 
				self.cur.executemany('insert into %s(state, action) values (?, ?)' % tablename, [(state, action) for action in actions]) 
				self.cur.execute('commit') 
			except sqlite3.Error:
				self.cur.execute("rollback")
				print("blah")
				raise

	def init_path(self, old_state, action, new_state, opponent=False):
		pass

	def learn_points(self, state, points):
		status=array_to_integer(status)
		s=self.statuses.get(status)
		if s is None:
			s=Status()
			self.statuses[status]=s
		s.minmax=points
		s.maxmin=points
		s.minmax_action=None 
		s.maxmin_action=None

	def calculate(self, id_, lvl=99):
		if lvl>0:
			default=0 # i consider that the min the other can do is 0
			s=self.statuses.get(id_)
			if s is not None:
				if self.verbose:
					print("Calculate %d" % id_)
				l=[]
				for i in s.lto.items(): # i need to take the max of it, so i'll update maxmin
					act=i[0]
					s2=self.statuses.get(i[1])
					if s2 is not None:
						self.calculate(i[1], lvl-1)
						if s2.maxmin is None:
							l.append((default, act))
						else:
							l.append((s2.maxmin, act))
					else:
						l.append((default, act))
				if len(l)>0:
					l=sorted(l)
					#if self.verbose:
					#	print("minmax list %s" % l)
					s.minmax_action=l[0][1]
					s.minmax=l[0][0] 
				l=[]
				default=2
				for i in s.lt.items(): # i need to take the max of it, so i'll update maxmin
					act=i[0]
					s2=self.statuses.get(i[1])
					if s2 is not None:
						self.calculate(i[1], lvl-1)
						if s2.minmax is None:
							l.append((default, act)) 
						else:
							l.append((s2.minmax, act))
					else:
						l.append((default, act))
				if len(l)>0:
					l=sorted(l, reverse=True)
					#if self.verbose:
					#	print("maxmin list %s" % l)
					s.maxmin_action=l[0][1]
					s.maxmin=l[0][0] 
				l=[]
		
	def print_tree_minmax(self, id_, action=-1, shift='', level_down=4): 
		res=[]
		if len(shift)>60:
			raise Exception("infinite loop")
		if id_ is None:
			res.append("%s\\ %d->??" % (shift, action))
		else:
			s=self.statuses.get(id_)
			if s is not None:
				res.append("%s\ %d->%d (min=%s, action=%s)" % (shift, action, id_, s.minmax, s.minmax_action))	
				level_down-=1
				if level_down==0:
					res.append("%s    \\..." % shift)
				else:
					for i in sorted(s.lto.items(), reverse=True):
						res+=self.print_tree_maxmin(i[1], i[0], shift+'    ', level_down)
			return res

	def print_tree_maxmin(self, id_, action=-1, shift='', level_down=4): 
		res=[]
		if len(shift)>60:
			raise Exception("infinite loop")
		if id_ is None:
			res.append("%s\ %d->??" % (shift, action))
		else:
			s=self.statuses.get(id_)
			if s is not None:
				res.append("%s\ %d->%d (max=%s, action=%s)" % (shift, action, id_, s.maxmin, s.maxmin_action))
				level_down-=1
				if level_down==0:
					res.append("%s    \\..." % shift)
				else:
					for i in sorted(s.lt.items()):
						res+=self.print_tree_minmax(i[1], i[0], shift+'    ', level_down) 
		return res
