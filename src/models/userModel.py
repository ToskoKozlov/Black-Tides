#!/usr/bin/env python
# -*- coding: utf-8 -*-

class userModel(object):

	# class variable shared by all instances
	self._username = ''
	self._password = ''
	self._email = ''
	
	# class constructor with arguments
	def __init__(self, data):
		# instance variable unique to each instance
		self.username = data['username']
		self.password = data['password']
		self.email = data['email']

	@property
	def username(self):
		return self._username

	@username.setter
	def username(self, value):
		self._username = value

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, value):
		self._password = value

	@property
	def email(self):
		return self._email

	@email.setter
	def email(self, value):
		self._username = value