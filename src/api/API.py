#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

import json
from lib.daos import DAOSql

response = {
	"status": 200,
	"description": "OK",
	"data": {}
}

app = Flask(__name__)

# endpoint for the creation of a new user
@app.route("/login", methods=['POST'])
def login():
	try:
		data = request.get_json(cache=False)
		if data:
			response['data']['user'] = data['user_name']
			response['data']['password'] = data['password']
			if data.has_key('email'):
				response['data']['email'] = data['email']
		else:
			status = 400
			response['status'] = status
			response['description'] = "Error: no data received"
	except Exception as e:
		status = 400
		response['status'] = status
		response['description'] = "Error: " + str(e)

	return json.dumps(response)

# endpoint for authentication with username (or e-mail) and password
@app.route("/signin", methods=['POST'])
def signin():

	try:
		data = request.get_json(cache=False)
		response['user'] = data['user_name']
		response['password'] = data['password']

	except:
		status = 400
		response['status'] = status
		response['description'] = "Error: no data received"

	return json.dumps(response)

if __name__ == "__main__":
	app.run(
		host = "0.0.0.0",
		port = 5050,
		debug = True
	)


