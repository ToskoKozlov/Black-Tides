#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Create n entries to adventurers table:
 - Table atributes:
 	- CLASS (Swordmaster, Rogue, War theurgist, Warlock)
 	- STR (strength)
 	- AGI (agility)
 	- INT (intelligence)
 	- MAG (magicka)
 	- VIT (vitality)
 	- BRA (bravery)
 	- RACE (human, elf, dwarf, orc)
Generates random values for attributes described avobe
'''

from lib.daos import DAOSql
from src.models import adventurerModel
from random import randint
import random


atributes = ['strength', 'agility', 'intelligence', 'magicka', 'vitality', 'bravery']
classes = ['rogue', 'sword_master', 'war_theurgist', 'warlock']
races = ['human', 'elf', 'orc', 'dwarf']

def createAdventurer():
	adventurer_data = {}
	
	# set random atribute values
	for atribute in atributes:
		adventurer_data[atribute] = randint(10,18)

	# set random class
	adventurer_data['adv_class'] = random.choice(classes)

	# set random race
	adventurer_data['race'] = random.choice(races)

	# adjust adventurer depending on class
	adventurer_data = adjustAdventurer(adventurer_data)

	# create adventurer object
	adventurer = adventurerModel.adventurerModel()

	# set adventurer with random atributes
	adventurer.init(adventurer_data)

	return adventurer


def adjustAdventurer(adventurer_data):
	# adjust according to race
	if adventurer_data['race'] == 'human':
		adventurer_data['bravery'] += 3
		
		atribute1 = random.choice(atributes)
		while atribute1 == 'bravery':
			atribute1 = random.choice(atributes)

		atribute2 = random.choice(atributes)
		while atribute2 == 'bravery' or atribute2 == atribute1:
			atribute2 = random.choice(atributes)

		atribute3 = random.choice(atributes)
		while atribute3 == 'bravery' or atribute3 == atribute1 or atribute3 == atribute2:
			atribute3 = random.choice(atributes)
		
		adventurer_data[atribute1] += 2
		adventurer_data[atribute2] -= 3
		adventurer_data[atribute3] -= 2

	elif adventurer_data['race'] == 'orc':
		adventurer_data['strength'] += 3
		adventurer_data['vitality'] += 2
		adventurer_data['magicka'] -= 2
		adventurer_data['intelligence'] -= 3

	elif adventurer_data['race'] == 'elf':
		adventurer_data['magicka'] += 3
		adventurer_data['agility'] += 2
		adventurer_data['strength'] -= 2
		adventurer_data['vitality'] -= 3

	elif adventurer_data['race'] == 'dwarf':
		adventurer_data['vitality'] += 3
		adventurer_data['strength'] += 2
		adventurer_data['magicka'] -= 2
		adventurer_data['agility'] -= 3

	# adjust according to class
	if adventurer_data['adv_class'] == 'rogue':
		adventurer_data['agility'] += 3
		adventurer_data['intelligence'] += 2
		adventurer_data['vitality'] -= 2
		adventurer_data['bravery'] -= 3
		adventurer_data['magicka'] = 0 # this class can not have magicka

	elif adventurer_data['adv_class'] == 'sword_master':
		adventurer_data['strength'] += 3
		adventurer_data['bravery'] += 2
		adventurer_data['agility'] -= 2
		adventurer_data['intelligence'] -= 3
		adventurer_data['magicka'] = 0 # this class can not have magicka

	elif adventurer_data['adv_class'] == 'war_theurgist':
		adventurer_data['vitality'] += 3
		adventurer_data['magicka'] += 2
		adventurer_data['strength'] -= 2
		adventurer_data['agility'] -= 3

	elif adventurer_data['adv_class'] == 'warlock':
		adventurer_data['magicka'] += 3
		adventurer_data['intelligence'] += 2
		adventurer_data['bravery'] -= 2
		adventurer_data['vitality'] -= 3

	return adventurer_data

db = DAOSql.DAOSql(dbhost = 'localhost', dbuser = 'root', dbpass = 'root', dbname = 'black_tides')
N = 995

# repeat n times
for n in xrange(0, N):
	# create adventurer
	adventurer = createAdventurer()

	# insert adventurer
	response = db.insertAdventurer(adventurer)

