#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.daos import DAOSql
from src.models import adventurerModel
import random

class gameManager(object):
	# class constructor with arguments
	def __init__(self):
		self.db = DAOSql.DAOSql(dbhost = 'localhost', dbuser = 'root', dbpass = 'root', dbname = 'black_tides')

	# get a random number of adventurers from database
	def getAdventurers(self, size = 1):
		
		response = {}
		
		if self.db:
			adventurers = []

			# generate random ids
			adventurerIDs = self.generateRandomIDs(size)
			
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
	'''
	TOOLS
	'''
	# returns a list of random integers with range [0-1000]
	def generateRandomIDs(self, size):
		randomList = [random.randint(1,1000) for r in xrange(size)]
		return randomList