#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.daos import DAOGame
from src.models import adventurerModel
from src.models import questModel
import random, datetime

class gameManager(object):
	# class constructor with arguments
	def __init__(self):
		self.db = DAOGame.DAOGame()

	# get a random number of adventurers from database
	def getAdventurers(self, size = 1):
		
		response = {}
		
		if self.db:
			adventurers = []
			# get last id to know the limit of the random id
			idLimit = self.db.getLastID('adventurer')
			
			# generate random ids
			adventurerIDs = self.generateRandomIDs(size, idLimit)
			
			for adventurerID in adventurerIDs:
				adventurer = adventurerModel.adventurerModel()
				dbadventurer = self.db.getAdventurer(adventurerID)
				adventurer.init(dbadventurer)
				adventurers.append(adventurer)
			
			if len(adventurers) > 0:
				response['status'] = 200
				response['description'] = 'OK'
				response['data'] = []
				for adventurer in adventurers:
					response['data'].append(adventurer.serialize())

			else:
				response['status'] = 500
				response['description'] = "Error: could not obtain any adventurers. "

		else:
			response['status'] = 500
			response['description'] = "Error: could not connect to database. "

		return response

	# get all adventurers of a player
	def getUserAdventurers(self, user_token):
		response = {}
		if self.db:
			userAdventurers = self.db.getUserAdventurers(user_token)
			adventurers = []
			for userAdventurer in userAdventurers:
				adventurer = adventurerModel.adventurerModel()
				dbadventurer = self.db.getAdventurer(userAdventurer['adventurer_id'])
				adventurer.init(dbadventurer)
				adventurers.append(adventurer)

			response['status'] = 200
			response['description'] = 'OK'
			response['data'] = []
			for adventurer in adventurers:
				response['data'].append(adventurer.serialize())
		else:
			response['status'] = 500
			response['description'] = 'Error: could not connect to database'

		return response

	# asign an adventurer to a user
	def buyAdventurer(self, user_token, adventurer_id):
		response = {}
		if adventurer_id > 0:
			if self.db:
				response = self.db.insertUserAdventurer(user_token, adventurer_id)
			else:
				response['status'] = 500
				response['description'] = 'Error: could not connect to database'
		else:
			response['status'] = 400
			response['description'] = 'Error: invalid adventurer ID'
		return response
	
	# get a random number of quests of a certain level
	def getQuests(self, size = 1):
		response = {}
		
		if self.db:
			quests = []

			# get last id to know the limit of the random id
			idLimit = self.db.getLastID('quest')

			# generate random ids
			questsIDs = self.generateRandomIDs(size, idLimit)
			
			for questID in questsIDs:
				quest = questModel.questModel()
				dbquest = self.db.getQuest(questID)
				if dbquest:
					quest.init(dbquest)
					quests.append(quest)
			
			if len(quests) > 0:
				response['status'] = 200
				response['description'] = 'OK'
				response['data'] = []
				for quest in quests:
					response['data'].append(quest.serialize())

			else:
				response['status'] = 500
				response['description'] = "Error: could not obtain any adventurers. "

		else:
			response['status'] = 500
			response['description'] = "Error: could not connect to database. "

		return response

	# start a quest wit id "questID", for user "user_token" with adventurers "adventurers"
	def startQuest(self, user_token, adventurers, questID):
		response = {}
		
		if self.db:
			# get quest wit id questID
			quest = questModel.questModel()
			quest.init(self.db.getQuest(questID))

			errors = False
			for advent in adventurers:
				if not errors:
					adventurer = adventurerModel.adventurerModel()
					adventurer.init(advent)

					try:
						# insert questID into user_adventurer table for each adventurer given
						result = self.db.updateUserAdventurer(user_token, adventurer, questID)
					except Exception, e:
						errors = True
						print str(e)

			if not errors and result:
				# calculate success rate
				successRate = self.getSuccessRate(adventurers, quest)
				
				# finishDate <- calculate finish date
				now = datetime.datetime.now()
				finishDate = (now + datetime.timedelta(0,0,0,0, quest.quest_time)).strftime('%Y-%m-%d %H:%M:%S')
				
				try:
					# insert into user_quest table (quest_id, user_token, date_finished, success_rate)
					self.db.insertUserQuest(user_token, questID, finishDate, successRate)
				except Exception, e:
					errors = True
					print str(e)
			
			if errors:
				response['status'] = 400
				response['description'] = 'Error: user ' + user_token + ' does not have adventurer ' + str(adventurer.id)
			else:
				response['status'] = 200
				response['description'] = 'OK'

		
		return response
	
	# get all current quests for a user
	def getUserQuests(self, user_token):
		response = {}
		if self.db:
			quests = {
				'completed': [],
				'in_progress': []
			}
			now = datetime.datetime.now()
			
			# get all user_quests
			userQuests = self.db.getUserQuests(user_token)
			
			for userQuest in userQuests:
				quest = questModel.questModel()
				quest.init(self.db.getQuest(userQuest['quest_id']))
				if (userQuest['date_finished'] - now).total_seconds() <= 0:
					# this quest is completed
					quests['completed'].append(quest.serialize())

				else:
					quests['in_progress'].append(quest.serialize())

			response['status'] = 200
			response['description'] = 'OK'
			response['data'] = quests
		else:
			response['status'] = 500
			response['description'] = 'Error: could not connect to database'

		return response

	'''
	TOOLS
	'''
	# returns a list of random integers with range [0-idLimit]
	def generateRandomIDs(self, size, idLimit):
		randomList = [random.randint(1, idLimit) for r in xrange(size)]
		return randomList

	# calculates the success rate of a certain quest with the adventurers given
	def getSuccessRate(self, adventurers, quest):
		successRate = 0.0
		attributes = ['strength', 'agility', 'intelligence', 'magicka', 'vitality', 'bravery']
		failure_acc = 0.0

		for attribute in attributes:
			attSum = 0 # summatory of each adventurer attribute
			questAttr = getattr(quest, attribute) # quest attribute to be reached
			
			for adventurer in adventurers:
				attSum += adventurer[attribute]
	
			# check if attSum is enough for the quest
			if attSum < questAttr:
				failure_acc += (100 - ((attSum * 100)/float(questAttr))) / 6.0 # divided by the number of attributes to distribute the failure
		
		successRate = float("{0:.2f}".format(100 - failure_acc))

		return successRate
