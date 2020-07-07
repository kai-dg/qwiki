#!/usr/bin/env python3
from peewee import *
import utils.globals as g
from utils.models import make_tables
import os
import json
if not os.path.isfile(g.JSON_NAME):
    with open(g.JSON_NAME, "w") as f:
        template = g.JSON_TEMPLATE
        json.dump(template, f)
        make_tables()


def read_json() -> dict:
	with open(g.JSON_NAME, "r") as f:
		return json.load(f)

def write_json(data):
	"""Data always needs to be modified from read_json()"""
	with open(g.JSON_NAME, "w") as f:
		json.dump(data, f)

def create_profile(name, notes):
	data = read_json()
	data["wikis"][name] = notes
	write_json(data)

def change_profile(name):
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
