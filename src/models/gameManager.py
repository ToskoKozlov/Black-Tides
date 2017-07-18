﻿#!/usr/bin/env python
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
			adventurersOnQuest = []
			for userAdventurer in userAdventurers:
				adventurer = adventurerModel.adventurerModel()
				adventurer.init(self.db.getAdventurer(userAdventurer['adventurer_id']))
				
				# check if this adventurer is on a quest
				if userAdventurer['on_quest'] > 0:
					adventurers.append(adventurer)
				else:
					adventurersOnQuest.append(adventurer)

			response['status'] = 200
			response['description'] = 'OK'
			response['data'] = {
				'idle': [],
				'on_quest':[]
			}
			for adventurer in adventurers:
				response['data']['idle'].append(adventurer.serialize())
			for adventurer in adventurersOnQuest:
				response['data']['on_quest'].append(adventurer.serialize())
		else:
			response['status'] = 500
			response['description'] = 'Error: could not connect to database'

		return response

	# asign an adventurer to a user
	def buyAdventurer(self, user_token, adventurer_id, gold):
		response = {}
		errors = False
		if adventurer_id > 0:
			if self.db:
				if gold > 0:
					# get player
					player = self.db.getPlayer(user_token)
					
					# subtract gold from player
					finalGold = player['gold'] - gold 
					
					# set new gold value
					updated = self.db.updatePlayerGold(user_token, gold)
				else:
					errors = True
					response['status'] = 400
					response['description'] = 'Error: gold must be greater than 0'
			else:
				errors = True
				response['status'] = 500
				response['description'] = 'Error: could not connect to database'
		else:
			errors = True
			response['status'] = 400
			response['description'] = 'Error: invalid adventurer ID'

		if not errors:
			if updated:
				response = self.db.insertUserAdventurer(user_token, adventurer_id)
			else:
				response['status'] = 400
				response['description'] = 'Error: player '+ user_token +' have not enough gold'

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
						result = self.db.updateUserAdventurer(user_token, adventurer.id, questID)
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

	# complete a quest for a player
	def completeQuest(self, user_token, questID):
		response = {}
		errors = False
		if self.db:
			# get player_quest
			playerQuest = self.db.getUserQuest(user_token, questID)
			
			if playerQuest:
				# check success
				success = self.checkSuccess(playerQuest['success_rate'])
				if success:
					player = self.db.getPlayer(user_token)	# get player information
					quest = self.db.getQuest(questID)		# get quest information
				
					# add gold 
					finalGold = player['gold'] + quest['gold']
					updated = self.db.updatePlayerGold(user_token, finalGold)

					if updated:
						# add influence
						finalInfluence = player['influence'] + quest['influence']
						updated = self.db.updatePlayerInfluence(user_token, finalInfluence)
						if not updated:
							errors = True
							response['status'] = 500
							response['description'] = "Error: could not update influence reward"
					else:
						errors = True
						response['status'] = 500
						response['description'] = "Error: could not update gold reward"
			else:
				errors = True
				response['status'] = 500
				response['description'] = "Error: user "+user_token+" does not have quest "+str(questID)

			if not errors:
				# remove entry on player_quests table
				if self.db.removePlayerQuest(user_token, questID):
					# release adventurers on player_adventurers
					userAdventurers = self.db.getUserAdventurers(user_token, questID)
					for userAdventurer in userAdventurers:
						adventurer = adventurerModel.adventurerModel()
						self.db.updateUserAdventurer(user_token, userAdventurer['adventurer_id'], 0)
					
					# return success and current gold and influence
					response['status'] = 200
					response['description'] = "OK"
					response['data'] = {
						'gold': finalGold,
						'influence': finalInfluence,
						'success': success
					}
				else:
					errors = True
					response['status'] = 500
					response['description'] = "Error: could not update gold reward"
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

	# check if a quest have success
	def checkSuccess(self, successRate):
		success = False
		
		if float("{0:.2f}".format(random.uniform(0,100))) <= successRate:
			success = True

		return success