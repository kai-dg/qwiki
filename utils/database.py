#!/usr/bin/env python3
import ui.settings as s
import os
import json
import sys
#ABSPATH = os.path.dirname(os.path.realpath(__file__))
#DB_INFO_PATH = os.path.join(ABSPATH, s.JSON_NAME)
if not os.path.isfile(s.JSON_NAME):
    with open(s.JSON_NAME, "w") as f:
        template = {"active": "", "wikis": {}}
        json.dump(template, f)

def read_json() -> dict:
	with open(s.JSON_NAME, "r") as f:
		return json.load(f)

def write_json(data):
	"""Data always needs to be modified from read_json()"""
	with open(s.JSON_NAME, "w") as f:
		json.dump(data, f)

def create_profile(name, notes):
	data = read_json()
	data["wikis"][name] = notes
	write_json(data)

def load_profile(name):
	data = read_json()
	data["active"] = name
	write_json(data)

def delete_profile(name):
	del data["wikis"][name]

def update_profile(name, new, notes):
	data = read_json()
	if new:
		temp = data["wikis"][name]
		data["wikis"][new] = temp
		del data["wikis"][name]
	if notes:
		data["wikis"][name] = notes
	write_json(data)