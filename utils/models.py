#!/usr/bin/env python3
"""Database stuff"""
from peewee import *
DB = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    class Meta:
        database = DB

class Page(BaseModel):
    """"""
    name = CharField(max_length=50)
    notes = TextField()
    image_path = CharField(max_length=50)
    image_title = CharField(max_length=50)
    
class Content(BaseModel):
    """Card content"""
    page = ForeignKeyField(Page)
    title = CharField(max_length=50)
    order = IntegerField()
    content = TextField()
    content_image = CharField(max_length=50)
    content_image_title = CharField(max_length=50)

if __name__ == "__main__":
    pass
