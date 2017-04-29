#!/usr/bin/env python
# -*- coding: utf-8 -*-

class adventurerModel(object):

	# class constructor with arguments
	def __init__(self):
		# instance variable unique to each instance
		self.id = None
		self._adv_class = ''
		self._strength = ''
		self._agility = ''
		self._intelligence = ''
		self._magicka = ''
		self._vitality = ''
		self._bravery = ''
		self._race = ''

	def init(self, data):
		self.id = data['id']
		self.adv_class = data['adv_class']
		self.strength = data['strength']
		self.agility = data['agility']
		self.intelligence = data['intelligence']
		self.magicka = data['magicka']
		self.vitality = data['vitality']
		self.bravery = data['bravery']
		self.race = data['race']

	def serialize(self):
		data = {}
		data['id'] = self.id
		data['adv_class'] = self.adv_class
		data['strength'] = self.strength
		data['agility'] = self.agility
		data['intelligence'] = self.intelligence
		data['magicka'] = self.magicka
		data['vitality'] = self.vitality
		data['bravery'] = self.bravery
		data['race'] = self.race
		return data

	@property
	def id(self):
		return self._id
	@id.setter
	def id(self, value):
		self._id = value

	@property
	def adv_class(self):
		return self._adv_class

	@adv_class.setter
	def adv_class(self, value):
		self._adv_class = value

	@property
	def strength(self):
		return self._strength

	@strength.setter
	def strength(self, value):
		self._strength = value
	
	@property
	def agility(self):
		return self._agility

	@agility.setter
	def agility(self, value):
		self._agility = value
	
	@property
	def intelligence(self):
		return self._intelligence

	@intelligence.setter
	def intelligence(self, value):
		self._intelligence = value
	
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
	def race(self):
		return self._race

	@race.setter
	def race(self, value):
		self._race = value