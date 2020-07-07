#!/usr/bin/env python3
from peewee import *
# FILES
JSON_NAME = "db_info.json"
DEFAULT_DB = "ADD A WIKI"
DB_FILE = ".qwiki.data"
DB = SqliteDatabase(DB_FILE)
# GLOBAL VARS
TARGET = None # Page object container
IDX = 0 # Content.idx tracker
PAGE_NAME = ""
CONTENT = {} # idx: {header: content}
WIKI_LIST = ["test1"]
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
