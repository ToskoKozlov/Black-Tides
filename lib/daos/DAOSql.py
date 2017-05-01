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
	DATABASE TOOLS
	'''
	# return a cursor
	def getCursor(self, query):
		if self.conn:
			cursor = self.conn.cursor()	# create a cursor
			cursor.execute(query)		# execute query
		return cursor

	# return a dictionary cursor
	def getDictCursor(self, query):
		if self.conn:
			cursor = self.conn.cursor(MySQLdb.cursors.DictCursor) # create a cursor
			cursor.execute(query)
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