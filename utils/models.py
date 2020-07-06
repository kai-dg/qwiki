#!/usr/bin/env python3
"""Database stuff"""
from peewee import *
import ui.settings as s
from utils.controller import ModelCtrl
from utils.controller import Query


class BaseModel(Model):
    class Meta:
        database = s.DB

class Content(BaseModel):
    """Wiki page's content model"""
    title = CharField(max_length=50)
    idx = IntegerField()
    content = TextField()
    content_img = CharField(max_length=50)
    content_img_title = CharField(max_length=50)

class Page(BaseModel):
    """Wiki page model"""
    name = CharField(max_length=50)
    notes = TextField()
    content = ManyToManyField(Content, backref="pages")
    img_path = CharField(max_length=50)
    img_title = CharField(max_length=50)
    tags = BooleanField(default=False)
    relations = BooleanField(default=False)

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

# Dynamic Models that can change db with ._meta.database
# Use these as the models instead of above
DPage = Page
DContent = Content
DTag = Tag
DDInfo = DatabaseInfo
DRelations = Relations

def models_db_swap():
    s.DB = SqliteDatabase(s.DB_FILE)
    DPage._meta.database = s.DB
    DContent._meta.database = s.DB
    DTag._meta.database = s.DB
    DDInfo._meta.database = s.DB
    DRelations._meta.database = s.DB

def make_tables():
    """Make preset database info here"""
    s.DB.create_tables([DDInfo, DPage, DContent, DTag, DRelations])
    s.DB.create_tables([DRelations.pages.get_through_model()])
    s.DB.create_tables([DTag.pages.get_through_model()])
    s.DB.create_tables([DPage.content.get_through_model()])
    DDInfo.create(set_tags="").save()

def set_ctrl():
    m = ModelCtrl(DPage, DContent, DTag, DDInfo, DRelations)
    return m

def set_query(name):
    q = Query(name, DPage, DRelations)
    return q
    