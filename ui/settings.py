#!/usr/bin/env python3
from peewee import *
# APP STUFF
TITLE = "Qwiki"
#COLORS
BG = "#0D0D0D"
BG2 = "#2C2C29" # dark
FG = "#30302C"
SEARCHBG = "#9C9984"
SEARCHFG = "#F7F5E4"
BUTTON_A = "#6ABAD7"
BUTTON_D = "#458EA9"
BUTTON_R = "#9A6767"
TEXT1 = "#FAF9EF" # light
TEXT2 = "#333332" # dark
TEXT3 = "#1D1D1C" # darker
#FONTS
FONT1 = "Courier"
NORMAL_FONT = "Arial"
#SIZES
W_HEIGHT = 750
W_WIDTH = 700
# GLOBAL VARS
TARGET = None
IDX = 0
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
MENU_BUTTONS = {} # For changing button colors
# FILES
JSON_NAME = "db_info.json"
DEFAULT_DB = "ADD WIKI"
#DB_FILE = ".data"
DB_FILE = "Test.db"
DB = SqliteDatabase(DB_FILE)
