#!/usr/bin/env python3
"""Formats input from user to be able to insert into database."""
import utils.globals as g
import re


def format_title(name:str) -> str:
    res = f"=== {name} ===\n"
    return res

def format_note(notes:str) -> str:
    res = f"{notes.rstrip()}"
    if res.split()[0] != "[Notes]" and res != "":
        m = re.search(r"[a-zA-Z]", notes)
        if m:
            notes = notes.replace(notes[m.start()], notes[m.start()].upper(), 1)
        res = f"[Notes] {notes.rstrip()}"
    return res

def format_header(header:str) -> str:
    if header[0] == "\n":
        header[0] = ""
    res = f"+ {header}\n"
    return res

def format_content(content:str) -> str:
    idx = 0
    res = content.rstrip().split("\n")
    for line in res:
        temp = line.rstrip()
        m = re.search(r"[a-zA-Z]", temp)
        if m:
            res[idx] = temp.replace(temp[m.start()], temp[m.start()].upper(), 1)
        else:
            res[idx] = temp
        idx += 1
    return "\n".join(res)