#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.daos import DAOSql

class loginManager(object):

	# class constructor with arguments
	def __init__(self):
		self.db = DAOSql.DAOSql(dbhost = 'localhost', dbuser = 'root', dbpass = 'root', dbname = 'black_tides')

	# create a new user in database
	def createUser(self, user):
		if self.db:
			response = self.db.insertUser(user)
		else:
			response['status'] = 500
			response['description'] = "Error: could not connect to database. "

		return response


