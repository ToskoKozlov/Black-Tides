#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.daos.DAOSql import DAOSql
import ConfigParser

class DAOGame(DAOSql):
    # class constructor with arguments
	def __init__(self):
		config = ConfigParser.RawConfigParser(allow_no_value=True)
		config.read('/etc/config/routesConfig.conf')
		self.dbuser = config.get('black_tides', 'user')
		self.dbpass = config.get('black_tides', 'pass')
		self.dbhost = config.get('black_tides', 'host')
		self.dbname = config.get('black_tides', 'dbname')
		
		super(DAOGame, self).__init__(dbhost = self.dbhost, dbuser = self.dbuser, dbpass = self.dbpass, dbname = self.dbname)

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
	GET METHODS
	'''
	# get an adventurer by id
	def getAdventurer(self, adventurerID):
		query = "SELECT * FROM `adventurer` WHERE `id`= %i" % (adventurerID)
		try:
			cursor = self.getDictCursor(query)
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
			cursor = self.getDictCursor(query)
		except Exception, e:
			print str(e)
			cursor = None

		if cursor:
			adventurers = cursor.fetchall()		# get all results

		return adventurers
	
	# get an item from user_quest table
	def getUserQuests(self, user_token):
		userQuests = []
		query = "SELECT * FROM `user_quest` WHERE `user_token`= '%s'" % (user_token)
		try:
			cursor = self.getDictCursor(query)
		except Exception, e:
			print str(e)
			cursor = None

		if cursor:
			userQuests = cursor.fetchall()		# get all results

		return userQuests

	# get a quest from database
	def getQuest(self, questID):
		quest = {}
		query = "SELECT * FROM `quest` WHERE `id`= %i" % (questID)
		try:
			cursor = self.getDictCursor(query)
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


