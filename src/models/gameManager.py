#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.daos import DAOSql

class gameManager(object):
	# class constructor with arguments
	def __init__(self):
		self.db = DAOSql.DAOSql(dbhost = 'localhost', dbuser = 'root', dbpass = 'root', dbname = 'black_tides')

	# get a random number of adventurers from database
	def getAdventurers(size = 1, user_token = ''):
		if self.db:
			adventurers = []
			# generate random ids
			adventurerIDs = generateRandomIDs(size)
			for adventurerID in adventurerIDs:
				adventurers.append(self.db.getAdventurer(adventurerID))
			if len(adventurers) > 0:
				response = self.db.setAdventurers(adventurers, user_token)
			else:
				response['status'] = 500
				response['description'] = "Error: could not obtain any adventurer. "
		else:
			response['status'] = 500
			response['description'] = "Error: could not connect to database. "

		return response

