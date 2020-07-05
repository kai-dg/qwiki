#!/usr/bin/env python3
"""Database stuff"""
from peewee import *
import ui.settings as s
from utils.controller import ModelCtrl


class BaseModel(Model):
    class Meta:
        database = s.DB

class Page(BaseModel):
    """Wiki page model"""
    name = CharField(max_length=50)
    notes = TextField()
    img_path = CharField(max_length=50)
    img_title = CharField(max_length=50)

class DatabaseInfo(BaseModel):
    """Always grab this by ID 0. Add more vars if needed.
    Vars:
        set_tags format ex: 'tag1,tag2,tag3
    """
    set_tags = TextField()

class Tag(BaseModel):
    name = CharField(max_length=25)
    page = ForeignKeyField(Page)

class Content(BaseModel):
    """Wiki page's content model"""
    page = ForeignKeyField(Page)
    title = CharField(max_length=50)
    idx = IntegerField()
    content = TextField()
    content_img = CharField(max_length=50)
    content_img_title = CharField(max_length=50)

# Dynamic Models that can change db with ._meta.database
# Use these as the models instead of above
DPage = Page
DContent = Content
DTag = Tag
DDInfo = DatabaseInfo

def models_db_swap():
    s.DB = SqliteDatabase(s.DB_FILE)
    DPage._meta.database = s.DB
    DContent._meta.database = s.DB
    DTag._meta.database = s.DB
    DDInfo._meta.database = s.DB

def make_tables():
    """Make preset database info here"""
    s.DB.create_tables([DDInfo, DPage, DContent, DTag])
    DDInfo.create(set_tags="").save()

def set_ctrl():
    m = ModelCtrl(DPage, DContent, DTag, DDInfo)
    return m