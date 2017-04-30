#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Create n entries to quests table:
 - Table atributes:
	- level
	- gold
	- influence
	- quest_type
	- strength
	- intelligence
	- agility
	- magicka
	- vitality
	- bravery
	- power
	- quest_time
Generates random values for attributes described avobe
'''
import random, sys, MySQLdb, json
sys.path.append('../../Black-Tides')
from lib.daos import DAOSql
from src.models import questModel
from random import randint

atributes = ['strength', 'agility', 'intelligence', 'magicka', 'vitality', 'bravery']
questTypes = ['escort', 'booty', 'purge', 'slay', 'summoning']

def createQuest(level):
	quest_data = {}
	power_base = 0

	quest_data['level'] = level

	# set random atribute values
	for atribute in atributes:
		if level == 1:
			quest_data[atribute] = randint(1,10)
		if level == 2:
			quest_data[atribute] = randint(10,25)
		if level == 3:
			quest_data[atribute] = randint(25,60)
		if level == 4:
			quest_data[atribute] = randint(60,150)
	
	# set random type
	quest_data['quest_type'] = random.choice(questTypes)
	
	# adjust adventurer depending on class
	quest_data = adjustQuest(quest_data)

	# time in minutes to complete the quest
	quest_data['quest_time'] = int(quest_data['power'] / 1.5)

	# create adventurer object
	quest = questModel.questModel()

	# set adventurer with random atributes
	quest.init(quest_data)

	return quest

def adjustQuest(quest_data):
	level = quest_data['level']

	# adjust according to type
	if quest_data['quest_type'] == 'escort':
		quest_data['vitality'] += int(level * 0.5)
		quest_data['intelligence'] += int(level * 1.5)
		quest_data['agility'] += level

		# calculate quest power
		quest_data['power'] = setPower(quest_data)
		
		# set base rewards (gold and influence)
		quest_data['gold'] = quest_data['power'] * 10
		quest_data['influence'] = quest_data['power'] * 4

	elif quest_data['quest_type'] == 'booty':
		quest_data['agility'] += int(level * 1.5)
		quest_data['bravery'] += level
		quest_data['strength'] += int(level * 0.5)
		quest_data['intelligence'] += int(level * 0.5)

		# calculate quest power
		quest_data['power'] = setPower(quest_data)
		
		# set base rewards (gold and influence)
		quest_data['gold'] = quest_data['power'] * 25
		quest_data['influence'] = quest_data['power'] * 2


	elif quest_data['quest_type'] == 'purge':
		quest_data['magicka'] += int(level * 0.5)
		quest_data['bravery'] += int(level * 1.5)
		quest_data['strength'] += int(level * 1.5)
		quest_data['vitality'] += level

		# calculate quest power
		quest_data['power'] = setPower(quest_data)
		
		# set base rewards (gold and influence)
		quest_data['gold'] = quest_data['power'] * 20
		quest_data['influence'] = quest_data['power'] * 4

	elif quest_data['quest_type'] == 'slay':
		quest_data['intelligence'] += level
		quest_data['magicka'] += int(level * 0.5)
		quest_data['agility'] += int(level * 1.5)

		# calculate quest power
		quest_data['power'] = setPower(quest_data)
		
		# set base rewards (gold and influence)
		quest_data['gold'] = quest_data['power'] * 20
		quest_data['influence'] = quest_data['power'] * 8
	
	elif quest_data['quest_type'] == 'summoning':
		quest_data['magicka'] += int(level * 1.5)
		quest_data['intelligence'] += level

		# calculate quest power
		quest_data['power'] = setPower(quest_data)
		
		# set base rewards (gold and influence)
		quest_data['gold'] = quest_data['power'] * 15
		quest_data['influence'] = quest_data['power'] * 4

	return quest_data

# calculates a quest power
def setPower(quest_data):
	power = 0

	power = quest_data['strength'] + quest_data['agility'] + quest_data['intelligence'] + quest_data['vitality'] + quest_data['magicka'] + quest_data['bravery']

	return power

db = DAOSql.DAOSql(dbhost = 'localhost', dbuser = 'root', dbpass = 'root', dbname = 'black_tides')
N = 150
quest_level = 4

data = ['localhost', 'root', 'root', 'black_tides']
conn = MySQLdb.connect(*data)

cursor = conn.cursor()	# create a cursor

# repeat n times
for n in xrange(0, N):
	# create adventurer
	quest = createQuest(quest_level)

	# insert adventurer
	response = db.insertQuest(quest)