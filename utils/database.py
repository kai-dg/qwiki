#!/usr/bin/env python3
import os
import json
import sys
ABSPATH = os.path.dirname(os.path.realpath(__file__))
DB_INFO = os.path.join(ABSPATH, "db_info.json")

def create_db_info():
    if not os.path.isfile(DB_INFO):
        name = input("A one word name for your database: ")
        if len(name.split()) != 1:
            sys.exit("Error >>> One word only.")
        name = f"{name}.db"
        notes = input("Database description/notes: ")
        with open(DB_INFO, "w") as f:
            data = {
                name: {
                    "active": True,
                    "notes": notes
                }
            }
            json.dump(data, f)
        return data
    else:
        sys.exit("Error >>> db_info.json already exists.")

def read_db_info():
    try:
        with open(DB_INFO, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return create_db_info()

def write_db_info(data):
    with open(DB_INFO, "w+") as f:
        json.dump(data, f)

def insert_db_info(name, active, notes, name_change=""):
    name = f"{name}.db"
    data = read_db_info()
    if name_change != "":
        data[f"{name_change}.db"] = data[name]
        del data[name]
        name = f"{name_change}.db"
    db_info = data[name]
    db_info["active"] = active if active != "" else db_info["active"]
    db_info["notes"] = notes if notes != "" else db_info["notes"]
    data[name] = db_info
    write_db_info(data)

def create_db_tables(db, tables):
    db.connect()
    db.create_tables(tables)
    print(">>> Initialized database for wiki, ready to use.")

def get_db_active():
    data = read_db_info()
    for name in data:
        if data[name]["active"] == True:
            return name

if __name__ == "__main__":
    pass
