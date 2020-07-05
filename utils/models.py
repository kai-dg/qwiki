#!/usr/bin/env python3
"""Database stuff"""
from peewee import *
import ui.settings as s


class BaseModel(Model):
    class Meta:
        database = s.DB

class Page(BaseModel):
    """"""
    name = CharField(max_length=50)
    notes = TextField()
    img_path = CharField(max_length=50)
    img_title = CharField(max_length=50)
    
class Content(BaseModel):
    """Page Content"""
    page = ForeignKeyField(Page)
    title = CharField(max_length=50)
    idx = IntegerField()
    content = TextField()
    content_img = CharField(max_length=50)
    content_img_title = CharField(max_length=50)

class Tag(BaseModel):
    page = ForeignKeyField(Page)
    name = CharField(max_length=50)

# Dynamic Models that can change db with ._meta.database
# Use these as the models instead of above
DPage = Page
DContent = Content
DTag = Tag

def models_db_swap():
    DPage._meta.database = s.DB
    DContent._meta.database = s.DB
    DTag._meta.database = s.DB

def make_tables():
    s.DB.create_tables([DPage, DContent, DTag])
