#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

import json

response = {
	"status": 200,
	"description": "OK"
}


app = Flask(__name__)

@app.route("/login", methods=['POST'])
def login():

	data = request.get_json()

	response['user'] = data['user_name']
	response['password'] = data['password']

	return json.dumps(response)

if __name__ == "__main__":
	app.run(
		host = "0.0.0.0",
		port = 5050,
		debug = True
	)


