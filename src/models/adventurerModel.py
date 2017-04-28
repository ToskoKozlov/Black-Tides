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
		self.adv_class = data['adv_class']
		self.strength = data['strength']
		self.agility = data['agility']
		self.intelligence = data['intelligence']
		self.magicka = data['magicka']
		self.vitality = data['vitality']
		self.bravery = data['bravery']
		self.race = data['race']
