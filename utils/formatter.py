#!/usr/bin/env python3
"""Formats input from user to be able to insert into database."""
import utils.globals as g
import re


def format_title(name:str) -> str:
    res = f"=== {name} ===\n"
    return res

def format_note(notes:str) -> str:
    res = f"{notes}\n"
    if notes != "":
        res = f"[Notes] {notes}\n"
    return res

def format_header(header:str) -> str:
    if header[0] == "\n":
        header[0] = ""
    res = f"+ {header}\n"
    return res

def format_content(content:str) -> str:
    res = ""
    splitted = content.rstrip().split("\n")
    for i in splitted:
        if i[0] != " " and i[0] != "\t":
            res += f"- {i.capitalize()}\n"
        else:
            m = re.search(r"[a-zA-Z]", i)
            first = i[m.start()]
            new = i.replace(i[m.start()], i[m.start()].upper(), 1)
            res += f"{new}\n"
    res += "\n"
    return res
