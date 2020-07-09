#!/usr/bin/env python3
from peewee import *
# DATABASE
DB_FILE = "Default.db"
DB = SqliteDatabase(DB_FILE)
DBP = DatabaseProxy()
DBP.initialize(DB) # Database connects when models.py gets imported from database.py
DEFAULT_DB = "Default" # Display name on screen
MODELCTRL = None
QUERY = None
# FILES/FOLDERS
JSON_NAME = "db_info.json"
JSON_TEMPLATE = {
	"active": "Default",
	"wikis": {
		"Default": "Change my name and description"
	}
}
BASE_IMG_FOLDER = "images"
# GLOBAL VARS
TARGET = "" # Page name holder
TARGET_PAGE = None # Page object holder
TARGET_PAGE_CONT = None # Page's content object holder
IDX = 0 # Content.idx tracker
PAGE_NAME = ""
CONTENT = {} # idx: {header: content}
WIKI_LIST = []
WIKI_DB_INFO = {}
PAGE_TEMPLATE = {
    "page": {
        "name": "",
        "notes": ""
    },
    "cont": {}, # cont format: {idx: {title: content}}
    "page_obj": None
}
TAB = "    "
MENU_BUTTONS = {} # ui/app.py -> App.bottom_buttons()
