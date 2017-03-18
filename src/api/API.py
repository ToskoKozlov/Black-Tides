#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

import json
from daos import DAOSql

response = {
	"status": 200,
	"description": "OK"
}

app = Flask(__name__)

# endpoint for the creation of a new user
@app.route("/login", methods=['POST'])
def login():
	try:
		data = request.get_json()
		response['user'] = data['user_name']
		response['password'] = data['password']
		response['email'] = data['email'] if data.has_key('email') else ''

	except:
		status = 400
		response['status'] = status
		response['description'] = "Error: no data received"

	return json.dumps(response)

# endpoint for authentication with username (or e-mail), password
@app.route("/signin", methods=['POST'])
def signin():

	try:
		data = request.get_json()
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


