#!/usr/bin/env python
# -*- coding: utf-8 -*-

class userModel(object):

	# class constructor with arguments
	def __init__(self, data):
		# instance variable unique to each instance
		self.id = None
		self._username = data['user_name']
		self._password = data['password']
		self._email = data['email'] if data.has_key('email') else ''

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
		self._email = value