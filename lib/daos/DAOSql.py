#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb, time

class DAOSql(object):

	# class constructor with arguments
	def __init__(self, **kwargs):
		# set connection arguments
		self.dbhost = kwargs.get('dbhost')
		self.dbuser = kwargs.get('dbuser')
		self.dbpass = kwargs.get('dbpass')
		self.dbname = kwargs.get('dbname')
		data = [self.dbhost, self.dbuser, self.dbpass, self.dbname]

		# check if it is not empty
		if data:
			self.conn = MySQLdb.connect(*data)	# connect to data base

	# insert a value into user table
	def insertUser(self, user):
		
		response = {}

		errors = False

		creationDate = time.strftime('%Y-%m-%d %H:%M:%S')

		query = "INSERT INTO user (username, email, password, creation_date, user_token, enabled) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (user.username, user.email, user.password, creationDate, user.user_token, 1)

		try:
			cursor = self.getCursor(query)
		except self.conn.IntegrityError:
			errors = True
			cursor = None
		
		if cursor:
			self.conn.commit()	# commit writting data
			cursor.close()		# close cursor 

		if not errors:
			response['status'] = 200
			response['description'] = 'OK'
		else:
			response['status'] = 400
			response['description'] = 'Error: user '+ user.username + ' already exists'
		return response


	# insert a new adventurer into adventurers table
	def insertAdventurer(self, adventurer):
		
		response = {}

		errors = False

		query = '''INSERT INTO 
					adventurer (class, strength, intelligence, agility, magicka, vitality, bravery, race) 
				VALUES 
					('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (adventurer.adv_class, adventurer.strength, adventurer.intelligence, adventurer.agility, adventurer.magicka, adventurer.vitality, adventurer.bravery, adventurer.race)

		try:
			cursor = self.getCursor(query)
		except self.conn.IntegrityError:
			errors = True
			cursor = None
		
		if cursor:
			self.conn.commit()	# commit writting data
			cursor.close()		# close cursor 

		if not errors:
			response['status'] = 200
			response['description'] = 'OK'
		else:
			response['status'] = 400
			response['description'] = 'Error: could not insert adventurer'
		return response


	# get a user from database
	def getUser(self, user):
		user_token = ''
		query = "SELECT user_token FROM `user`"

		if user.email:
			query = query + " WHERE `email`= '%s' AND `password`= '%s'" % (user.email, user.password)
		else:
			query = query + " WHERE `username`= '%s' AND `password`= '%s'" % (user.username, user.password)

		try:
			cursor = self.getCursor(query)
		except Exception, e:
			print str(e)
			cursor = None

		if cursor:
			user_token = cursor.fetchone()	# get all results and keep only the first
			cursor.close()						# close cursor 

		return user_token

	# return a cursor
	def getCursor(self, query):

		if self.conn:
			cursor = self.conn.cursor()	# create a cursor
			cursor.execute(query)		# execute query
		return cursor