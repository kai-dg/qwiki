#!/usr/bin/env python3
from peewee import *
import sys
import utils.database as db
from utils.models import Card
from utils.models import Content
from utils.models import Subcontent
TABLES = [Card, Content, Subcontent]

def setup():
    name = db.get_db_active()
    database = SqliteDatabase(name)
    db.create_db_tables(database, TABLES)

if __name__ == "__main__":
    setup()
