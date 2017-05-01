#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, re

sys.path.append('../../Black-Tides')

from flask import Flask
from flask import request

import json
from src.models import loginManager
from src.models import gameManager
from src.models import userModel

# flask init
app = Flask(__name__)

# endpoint for the creation of a new user
@app.route("/user", methods=['POST'])
def create_user():
	# response template
	response = {
		"status": 200,
		"description": "OK",
		"data": {}
	}
	errors = False

	try:
		data = request.get_json(cache=False)	# read request data
	except Exception as e:
		errors = True
		response['status'] = 400
		response['description'] = "Error: " + str(e)

	if not errors:
		user = userModel.userModel()
		user.init(data)
		manager = loginManager.loginManager()
		response = manager.createUser(user)
	else:
		status = 400
		response['status'] = status
		response['description'] = "Error: no data received"

	if not errors and response['status'] == 200:
		status = 201
		response['status'] = status
		response['description'] = "User succesfully created"
	else:
		response['status'] = response['status']
		response['description'] = response['description']

	return json.dumps(response)


# endpoint for authentication with username (or e-mail) and password
@app.route("/login", methods=['POST'])
def login():
	# response template
	response = {
		"status": 200,
		"description": "OK",
		"data": {}
	}

	errors = False

	try:
		data = request.get_json(cache=False)	# read request data
	except Exception as e:
		errors = True
		response['status'] = 400
		response['description'] = "Error: " + str(e)

	if not errors:
		user = userModel.userModel()
		user.init(data)
		manager = loginManager.loginManager()
		response = manager.loginUser(user)

	if errors or response['status'] != 200:
		response['status'] = response['status']
		response['description'] = response['description']

	return json.dumps(response)

# endpoint to get a random number of adventurers
@app.route("/adventurers", methods=['GET'])
def getAdventurers():
	# response template
	response = {
		"status": 200,
		"description": "OK",
		"data": {}
	}
	errors = False

	# get size parameter
	size = int(request.args.get('size')) if request.args.get('size') else 1

	manager = gameManager.gameManager()
	response = manager.getAdventurers(size)

	if errors or response['status'] != 200:
		response['status'] = response['status']
		response['description'] = response['description']

	return json.dumps(response)

# get all adventurers for a player
@app.route("/user_token/<user_token>/adventurers", methods=['GET'])
def getUserAdventurers(user_token):
	# response template
	response = {
		"status": 200,
		"description": "OK",
		"data": {}
	}
	errors = False
	if re.match('[A-Fa-f0-9]{64}',user_token):
		manager = gameManager.gameManager()
		response = manager.getUserAdventurers(user_token)
	else:
		errors = True
		response['status'] = 400
		response['description'] = 'Error: user_token must be a sha256'

	return json.dumps(response)

# asign an adventurer to a player
@app.route("/user_token/<user_token>/adventurers/<int:adventurer_id>", methods=['POST'])
def buyAdventurer(user_token, adventurer_id):
	# response template
	response = {
		"status": 200,
		"description": "OK",
		"data": {}
	}
	errors = False
	if re.match('[A-Fa-f0-9]{64}',user_token):
		manager = gameManager.gameManager()
		response = manager.buyAdventurer(user_token, adventurer_id)
	else:
		errors = True
		response['status'] = 400
		response['description'] = 'Error: user_token must be a sha256'

	return json.dumps(response)

# endpoint to get a random number of quests
@app.route("/quests", methods=['GET'])
def getQuests():
	# response template
	response = {
		"status": 200,
		"description": "OK",
		"data": {}
	}
	errors = False

	# get size parameter
	size = int(request.args.get('size')) if request.args.get('size') else 1

	manager = gameManager.gameManager()
	response = manager.getQuests(size)

	if errors or response['status'] != 200:
		response['status'] = response['status']
		response['description'] = response['description']

	return json.dumps(response)

# endpoint to start a quest
@app.route("/user_token/<user_token>/quests/<int:questID>", methods=['POST'])
def startQuest(user_token, questID):
	# response template
	response = {
		"status": 200,
		"description": "OK",
		"data": {}
	}
	errors = False

	try:
		# check adventurers
		data = request.get_json(cache=False)	# read request data
	except Exception, e:
		errors = True
		response['status'] = 404
		response['description'] = "Error: request parameters not found " + str(e)

	if not errors:
		adventurers = data['adventurers'] if data.has_key('adventurers') else []
		
		if adventurers:
			manager = gameManager.gameManager()
			response = manager.startQuest(user_token, adventurers, questID)
		else:
			response['status'] = 404
			response['description'] = "Error: adventurers parameters not found"

	if errors or response['status'] != 200:
		response['status'] = response['status']
		response['description'] = response['description']

	return json.dumps(response)




if __name__ == "__main__":
	app.run(
		host = "0.0.0.0",
		port = 5050,
		debug = True
	)


