#!/usr/bin/env python3
"""Database stuff"""
from peewee import *
from utils.database import get_db_active
DB_NAME = get_db_active()
DB = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    class Meta:
        database = DB

class Card(BaseModel):
    """Every card creation comes with 1 subcard"""
    name = CharField(max_length=50)
    notes = TextField()
    card_format = CharField(max_length=50)
    images = BooleanField(default=False)

class Content(BaseModel):
    """Card content"""
    card = ForeignKeyField(Card)
    title = CharField(max_length=50)
    content = TextField()
    subcontent = BooleanField(default=False)

class Subcontent(BaseModel):
    """Card content's content"""
    card = ForeignKeyField(Content)
    title = CharField(max_length=50)
    content = TextField()

class Image(BaseModel):
    """Future implementation"""
    card = ForeignKeyField(Card, null=True)
    content = ForeignKeyField(Content, null=True)
    subcontent = ForeignKeyField(Subcontent, null=True)
    path = CharField(max_length=150)
    title = CharField(max_length=50)

if __name__ == "__main__":
    pass
