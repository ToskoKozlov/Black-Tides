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

	'''
	INSERT FUNCTIONS
	'''
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

	# add an adventurer to a user
	def insertUserAdventurer(self, user_token, adventurerID):
		response = {}

		errors = False

		query = '''INSERT INTO 
					user_adventurers (user_token, adventurer_id) 
				VALUES 
					('%s', '%s')''' % (user_token, adventurerID)

		try:
			cursor = self.getCursor(query)
		except self.conn.IntegrityError:
			errors = True
			cursor = None
		
		if cursor:
			self.conn.commit()	# commit writting data

		if not errors:
			response['status'] = 200
			response['description'] = 'OK'
		else:
			response['status'] = 400
			response['description'] = 'Error: could not insert adventurer'
		return response

	# insert a quest in database
	def insertQuest(self, quest):
				
		response = {}

		errors = False

		query = '''INSERT INTO 
					quest (
						level, 
						gold, 
						influence, 
						quest_type, 
						strength, 
						intelligence, 
						agility, 
						magicka, 
						vitality, 
						bravery, 
						power,
						quest_time
					) 
				VALUES 
					('%i', '%i', '%i', '%s', '%i', '%i', '%i', '%i', '%i', '%i', '%i', '%i')
				''' % (quest.level, quest.gold, quest.influence, quest.quest_type, quest.strength, quest.intelligence, quest.agility, quest.magicka, quest.vitality, quest.bravery, quest.power, quest.quest_time)

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
			response['description'] = 'Error: could not insert quest'
		return response
	
	# create a new entry in user_quest table
	def insertUserQuest(self, user_token, questID, finishDate, successRate):
		response = {}

		errors = False

		query = '''INSERT INTO 
					user_quest (user_token, quest_id, date_finished, success_rate) 
				VALUES 
					('%s', %i, '%s', %f)''' % (user_token, questID, finishDate, successRate)
		try:
			cursor = self.getCursor(query)
		except self.conn.IntegrityError:
			errors = True
			cursor = None
		
		if cursor:
			self.conn.commit()	# commit writting data

		if not errors:
			response['status'] = 200
			response['description'] = 'OK'
		else:
			response['status'] = 400
			response['description'] = 'Error: could not insert user_quest element'
		return response

	'''
	GET FUNCTIONS
	'''
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

	# get an adventurer by id
	def getAdventurer(self, adventurerID):
		query = "SELECT * FROM `adventurer` WHERE `id`= %i" % (adventurerID)
		try:
			if self.conn:
				cursor = self.conn.cursor (MySQLdb.cursors.DictCursor) # create a cursor
				cursor.execute(query)
		except Exception, e:
			print str(e)
			cursor = None

		if cursor:
			adventurer = cursor.fetchone()		# get all results and keep only the first

		return adventurer
	
	# get an item from user_adventurers table
	def getUserAdventurers(self, userToken):
		adventurers = []
		query = "SELECT * FROM `user_adventurers` WHERE `user_token`= '%s'" % (userToken)
		try:
			if self.conn:
				cursor = self.conn.cursor (MySQLdb.cursors.DictCursor) # create a cursor
				cursor.execute(query)
		except Exception, e:
			print str(e)
			cursor = None

		if cursor:
			adventurers = cursor.fetchall()		# get all results

		return adventurers
	
	# get a quest from database
	def getQuest(self, questID):
		query = "SELECT * FROM `quest` WHERE `id`= %i" % (questID)
		try:
			if self.conn:
				cursor = self.conn.cursor (MySQLdb.cursors.DictCursor) # create a cursor
				cursor.execute(query)
		except Exception, e:
			print str(e)
			cursor = None

		if cursor:
			quest = cursor.fetchone()		# get all results and keep only the first

		return quest

	'''
	UPDATES
	'''
	# add questID to user-adventurer table
	def updateUserAdventurer(self, user_token, adventurer, questID):
		query = "UPDATE `user_adventurers` SET on_quest=%i WHERE `user_token`='%s' AND `adventurer_id`=%i" % (questID, user_token, adventurer.id)

		try:
			cursor = self.getCursor(query)
		except Exception, e:
			print str(e)
			cursor = None

		if cursor:
			self.conn.commit()	# commit writting data

		return cursor


	'''
	DATABASE TOOLS
	'''
	# return a cursor
	def getCursor(self, query):
		if self.conn:
			cursor = self.conn.cursor()	# create a cursor
			cursor.execute(query)		# execute query
		return cursor

	# closes connection with database
	def closeConn(cursor):
		cursor.close()		# close cursor 

	# return the last id of a table
	def getLastID(self, tableName):
		lastID = 0
		query = "SELECT id FROM %s ORDER BY id DESC LIMIT 1" % tableName
		
		if self.conn:
			cursor = self.getCursor(query) # create a cursor
			lastID = cursor.fetchone()[0]

		return lastID