#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.daos.DAOSql import DAOSql
import ConfigParser, time

class DAOLogin(DAOSql):
    # class constructor with arguments
	def __init__(self):
		config = ConfigParser.RawConfigParser(allow_no_value=True)
		config.read('/etc/config/routesConfig.conf')
		self.dbuser = config.get('black_tides_login', 'user')
		self.dbpass = config.get('black_tides_login', 'pass')
		self.dbhost = config.get('black_tides_login', 'host')
		self.dbname = config.get('black_tides_login', 'dbname')
		
		super(DAOLogin, self).__init__(dbhost = self.dbhost, dbuser = self.dbuser, dbpass = self.dbpass, dbname = self.dbname)

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