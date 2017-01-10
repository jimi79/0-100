#!/usr/bin/python3

import importlib
import os
import pickle
import random
import sqlite3

class AI: 
	def __init__(self, dbname):
		self.conn=sqlite3.connect(dbname, isolation_level=None)
		self.cur=self.conn.cursor()
		self.verbose=False

	def init_db(self):
		self.cur.execute('create table my_states(state integer, maxmin integer, action integer);')
		self.cur.execute('create unique index idx_my_states on my_states(state)');
		self.cur.execute('create table opp_states(state integer, minmax integer, action integer);')
		self.cur.execute('create unique index idx_opp_states on opp_states(state)');
		self.cur.execute('create table lt(old_state integer, action action integer, new_state integer, opponent boolean);')
		self.cur.execute('create unique index idx_lt_old_state on lt(old_state, opponent, action)');
		self.cur.execute('create unique index idx_lt_new_state on lt(new_state, opponent, action)');

	def play(self, state, actions): 
		d=self.cur.execute("select action, maxmin from my_states where state=?", (state,)).fetchone()
		if d[0] is None:
			if self.verbose:
				print("Picked an action at random")
			action=random.choice(actions)
		else:
			action=d[0]
			if d[1] is None:
				if self.verbose:
					print("Picked an action to test somethg new") 
		return action

	def init_state(self, state, actions, opponent):
		if opponent:
			tablename='opp_states'
		else:
			tablename='my_states'
		self.cur.execute('select count(1) from %s where state = ?;' % tablename, (state, ))
		d=self.cur.fetchone()
		if d[0]==0: 
			self.cur.execute('begin')
			try:
				self.cur.execute('insert into %s(state) values (?);' % tablename, (state, ))
				self.cur.executemany('insert into lt(old_state, action, opponent) values (?, ?, ?)', [(state, action, opponent) for action in actions]) 
				self.cur.execute('commit') 
			except sqlite3.Error:
				self.cur.execute("rollback")
				raise

	def init_path(self, old_state, action, new_state, opponent):
		self.cur.execute('update lt set new_state=? where old_state=? and action=? and opponent=?;', (new_state, old_state, action, opponent))

	def init_points(self, state, points, opponent):
		if opponent:
			tablename='opp_states'
			col='minmax'
		else:
			tablename='my_states' 
			col='maxmin'
		self.cur.execute('update %s set %s=? where state=?;' % (tablename, col), (points, state))

	def calculate(self, state, opponent):
		# we calculate ourself, and the the parents
		if self.verbose:
			print("Calculating state %d for %s" % (state, ['myself', 'opponent'][opponent]))
		if opponent==True: # that is the opponent turn, so i check the minmax (it will try to minimize my points) 
			table="opp_states"
			other_table="my_states"
			mm="minmax"
			other_mm="maxmin"
			desc=""
		else: 
			table="my_states"
			other_table="opp_states"
			mm="maxmin"
			other_mm="minmax"
			desc="desc"

		action=None
		d=self.cur.execute("select action from lt where old_state=? and new_state is null;", (state,)).fetchone()
		if d is not None: # at least one record
			action=d[0]
		# if there is no result, perhaps we got a mm that is null (would be a repercution of an unknwon path
		d=self.cur.execute("select lt.action from lt inner join %s as s on lt.new_state=s.state where old_state=? and s.%s is null;" % (other_table, other_mm), (state,)).fetchone()
		if d is not None: # at least one record
			action=d[0]

		if action is not None: 
			sql="update opp_states set action=? where state=?" # we don't know its outcome, so we store it as being the best
			self.cur.execute(sql, (action, state))
			if self.verbose:
				print("u opp action=%d, state=%d" % (action, state))
		else: 
			sql="select lt.action, s.%s as mm from %s s inner join lt on lt.new_state=s.state and lt.opponent=1 where lt.old_state=? and not %s is null order by %s %s limit 1;" % (other_mm, other_table, other_mm, other_mm, desc)
			d=self.cur.execute(sql, (state,)).fetchone()
			if d is not None:
				action=d[0]
				mm_val=d[1] 
				sql="update %s set %s=?, action=? where state=?" % (table, mm)
				self.cur.execute(sql, (mm_val, action, state))
				if self.verbose:
					print("u %s minmax=%d, action=%d, state=%d" % (table, mm_val, action, state))

	def is_over(self):
		d=self.cur.execute('select count(1) from lt where new_state is null;').fetchone()[0]
		return d==0
