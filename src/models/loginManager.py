#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.daos import DAOLogin
from lib.daos import DAOGame
from src.models import userModel, gameManager
import bcrypt, random

class loginManager(object):

	# class constructor with arguments
	def __init__(self):
		self.dbLogin = DAOLogin.DAOLogin()
		self.dbGame = DAOGame.DAOGame()

	# create a new user in database
	def createUser(self, data):
		response = {}
		response['data'] = {}
		if self.dbLogin:
			user = userModel.userModel()
			user.init(data)
			if user.username and user.email:
				user.password = user.encryptPassword(user.password)
				response = self.dbLogin.insertUser(user)
			else:
				response['status'] = 400
				response['description'] = "Error: user must have username and email defined"
		else:
			response['status'] = 500
			response['description'] = "Error: could not connect to database"

		if response['status'] == 200:  # there is no errors
			# save new entry for player
			if self.dbGame:
				response = self.dbGame.insertPlayer(user.user_token)
				response['data'] = {"user_token": user.user_token}

				# generate three random initial adventurers
				gManager = gameManager.gameManager();
				adventurers = gManager.getAdventurers(3, True)

				for adventurer in adventurers:
					self.dbGame.insertUserAdventurer(user.user_token, adventurer.id, adventurer.name)

		return response

	# check if a user exists in database
	def loginUser(self, data):
		response = {}
		response['data'] = {}
		if self.dbLogin:
			user = userModel.userModel()
			user.init(data)
			result = self.dbLogin.getUser(user)

			if result:
				if self.passWordCorrect(user.password, result['password']):
					response['data']['user_token'] = result['user_token']
					response['status'] = 200
					response['description'] = 'OK'
				else:
					response['status'] = 401
					response['description'] = 'Error: Wrong password'
			else:
				response['status'] = 404
				response['description'] = 'Error: user ' + user.username + ' not found'
		else:
			response['status'] = 500
			response['description'] = "Error: could not connect to database"
		return response

	# check if clear password and hashed password are the same
	def passWordCorrect(self, clearPass, hashedPass):
		return bcrypt.hashpw(clearPass.encode('utf-8'), hashedPass) == hashedPass

	# returns a list of random integers with range [0-idLimit]
	def generateRandomIDs(self, size, idLimit):
		randomList = [random.randint(1, idLimit) for r in xrange(size)]
		return randomList