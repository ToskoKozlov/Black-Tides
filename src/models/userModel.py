#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, datetime

class userModel(object):

	# class constructor with arguments
	def __init__(self):
		# instance variable unique to each instance
		self._username = ''
		self._email = ''
		self._password = ''
		self._creation_date = datetime.time(0,0)
		self._user_token = ''
		self._enabled = 0


	def init(self, data):
		self.username = data['user_name']
		self.email = data['email'] if data.has_key('email') else ''
		self.password = data['password']

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

	@property
	def creation_date(self):
		return self._creation_date

	@creation_date.setter
	def creation_date(self, value):
		self._creation_date = value

	@property
	def user_token(self):
		return self._user_token

	@user_token.setter
	def user_token(self, value):
		self._user_token = value

	@property
	def enabled(self):
		return self._enabled

	@enabled.setter
	def enabled(self, value):
		self._enabled = value