#!/usr/bin/env python3
"""All db_info.json related functions"""
from peewee import *
import utils.globals as g
from utils.images import initial_base_folder
from utils.models import make_tables
import os
import json
if not os.path.isfile(g.JSON_NAME):
    with open(g.JSON_NAME, "w") as f:
        template = g.JSON_TEMPLATE
        json.dump(template, f)
        make_tables()
        initial_base_folder()


def read_json() -> dict:
	"""Returns db_info.json"""
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
	data = read_json()
	del data["wikis"][name]
	write_json(data)

def update_profile_name(new):
	data = read_json()
	temp_notes = data["wikis"][g.DEFAULT_DB]
	data["wikis"][new] = temp_notes
	del data["wikis"][g.DEFAULT_DB]
	write_json(data)
	change_profile(new)

def update_profile_desc(desc):
	g.WIKI_DB_INFO["wikis"][g.DEFAULT_DB] = desc
	write_json(g.WIKI_DB_INFO)
	g.WIKI_DB_INFO = read_json()