#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.daos import DAOLogin
from lib.daos import DAOGame
from src.models import userModel

class loginManager(object):

	# class constructor with arguments
	def __init__(self):
		self.dbLogin = DAOLogin.DAOLogin()
		self.dbGame = DAOGame.DAOGame()

	# create a new user in database
	def createUser(self, data):
	
		response = {}
		
		if self.dbLogin:
			user = userModel.userModel()
			user.init(data)
			if user.username and user.email:
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
		return response

	# check if a user exists in database
	def loginUser(self, data):
		response = {}
		if self.dbLogin:
			user = userModel.userModel()
			user.init(data)
			user_token = self.dbLogin.getUser(user)
			if user_token:
				response['user_token'] = user_token
				response['status'] = 200
				response['description'] = 'OK'
			else:
				response['status'] = 404
				response['description'] = 'Error: user ' + user.username + ' not found'
		else:
			response['status'] = 500
			response['description'] = "Error: could not connect to database"

		return response
