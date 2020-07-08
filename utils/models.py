#!/usr/bin/env python3
"""Database stuff"""
from peewee import *
import utils.database as db
import utils.globals as g
from utils.controller import ModelCtrl
from utils.controller import Query
import os
# Open app -> no database yet

class BaseModel(Model):
    class Meta:
        database = g.DBP

class Page(BaseModel):
    """Wiki page model"""
    name = CharField(unique=True, max_length=50)
    notes = TextField()
    img_path = CharField(max_length=50)
    img_title = CharField(max_length=50)
    tags = BooleanField(default=False)
    relations = BooleanField(default=False)

class Content(BaseModel):
    """Wiki page's content model"""
    page = ForeignKeyField(Page)
    title = CharField(max_length=50)
    idx = IntegerField()
    content = TextField()
    content_img = CharField(max_length=50)
    content_img_title = CharField(max_length=50)

class DatabaseInfo(BaseModel):
    """Always grab this by ID 0. Add more vars if needed.
    Vars:
        set_tags format ex: 'tag1,tag2,tag3
    """
    set_tags = TextField()

class Tag(BaseModel):
    name = CharField(max_length=25)
    pages = ManyToManyField(Page, backref="tags")

class Relations(BaseModel):
    """To link to related pages on a page."""
    page = ForeignKeyField(Page)
    pages = ManyToManyField(Page, backref="pages")

def change_database(name):
    """Changes current database to `name`"""
    g.DB_FILE = f"{name}.db"
    if not g.DB.is_closed():
        g.DB.close()
    g.DB = SqliteDatabase(g.DB_FILE)
    g.DB.connect()
    g.DBP.initialize(g.DB)

def make_tables():
    """Make preset database info here"""
    g.DB.create_tables([DatabaseInfo, Page, Content, Tag, Relations])
    g.DB.create_tables([Relations.pages.get_through_model()])
    g.DB.create_tables([Tag.pages.get_through_model()])
    DatabaseInfo.create(set_tags="").save()

def set_ctrl():
    m = ModelCtrl(Page, Content, Tag, DatabaseInfo, Relations)
    return m

def set_query(name:str):
    q = Query(name, Page, Content, Relations)
    return q
    
def init_database_info():
    g.WIKI_DB_INFO = db.read_json()
    g.DEFAULT_DB = g.WIKI_DB_INFO["active"]
    g.DB_FILE = f"{g.DEFAULT_DB}.db"
    g.WIKI_LIST = list(g.WIKI_DB_INFO["wikis"])
    g.WIKI_LIST = [""] if g.WIKI_LIST == [] else g.WIKI_LIST

def rename_database():
    if not g.DB.is_closed():
        g.DB.close()
    try:
        os.rename(g.RENAME_DB_TARGET, g.RENAME_DB_NEW)
    except:
        pass

def delete_database():
    """Close connection, delete file, check json if wiki list is empty,
    if empty, recreate default database, else switch to next db in ['wiki'],
    rename globals to newly switched db
    """
    if not g.DB.is_closed():
        g.DB.close()
    if os.path.isfile(g.DB_FILE):
        os.remove(g.DB_FILE)
    db.delete_profile(g.DEFAULT_DB)
    if g.WIKI_LIST != []:
        for name in g.WIKI_LIST:
            if name != g.DEFAULT_DB:
                g.DEFAULT_DB = name
                change_database(name)
                break
    else:
        g.DEFAULT_DB = "Default"
        change_database("Default")
        make_tables()
    db.change_profile(name)
    init_database_info()