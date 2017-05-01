#!/usr/bin/env python
# -*- coding: utf-8 -*-

class questModel(object):

	# class constructor
	def __init__(self):
		# instance variable unique to each instance
		self._id = None
		self._level = None
		self._gold = None
		self._influence = None
		self._quest_type = ''
		self._strength = None
		self._intelligence = None
		self._agility = None
		self._magicka = None
		self._vitality = None
		self._bravery = None
		self._power = None
		self._quest_time = None

	# class constructor with arguments
	def init(self, data):
		self.id = data['id'] if data.has_key('id') else 0
		self.level = data['level']
		self.gold = data['gold']
		self.influence = data['influence']
		self.quest_type = data['quest_type']
		self.strength = data['strength']
		self.intelligence = data['intelligence']
		self.agility = data['agility']
		self.magicka = data['magicka']
		self.vitality = data['vitality']
		self.bravery = data['bravery']
		self.power = data['power']
		self.quest_time = data['quest_time']

	# convert object to printable dictionary
	def serialize(self):
		data = {}
		data['id'] = self.id
		data['level'] = self.level
		data['gold'] = self.gold
		data['influence'] = self.influence
		data['quest_type'] = self.quest_type
		data['strength'] = self.strength
		data['agility'] = self.agility
		data['intelligence'] = self.intelligence
		data['magicka'] = self.magicka
		data['vitality'] = self.vitality
		data['bravery'] = self.bravery
		data['power'] = self.power
		data['quest_time'] = self.quest_time
		return data

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, value):
		self._id = value

	@property
	def level(self):
		return self._level

	@level.setter
	def level(self, value):
		self._level = value

	@property
	def gold(self):
		return self._gold

	@gold.setter
	def gold(self, value):
		self._gold = value

	@property
	def influence(self):
		return self._influence

	@influence.setter
	def influence(self, value):
		self._influence = value

	@property
	def quest_type(self):
		return self._quest_type

	@quest_type.setter
	def quest_type(self, value):
		self._quest_type = value

	@property
	def strength(self):
		return self._strength

	@strength.setter
	def strength(self, value):
		self._strength = value

	@property
	def intelligence(self):
		return self._intelligence

	@intelligence.setter
	def intelligence(self, value):
		self._intelligence = value

	@property
	def agility(self):
		return self._agility

	@agility.setter
	def agility(self, value):
		self._agility = value

	@property
	def magicka(self):
		return self._magicka

	@magicka.setter
	def magicka(self, value):
		self._magicka = value

	@property
	def vitality(self):
		return self._vitality

	@vitality.setter
	def vitality(self, value):
		self._vitality = value

	@property
	def bravery(self):
		return self._bravery

	@bravery.setter
	def bravery(self, value):
		self._bravery = value

	@property
	def power(self):
		return self._power

	@power.setter
	def power(self, value):
		self._power = value

	@property
	def quest_time(self):
		return self._quest_time

	@quest_time.setter
	def quest_time(self, value):
		self._quest_time = value
