#!/usr/bin/env python3
"""Wiki Settings

TODO:
    Display Label above Edit Wiki showing which Database is targeted.
    Display Label above import showing which is loaded.
        import button changes to normal if loaded
    Reorder left side:
        Wiki Name:
"""
from peewee import *
import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from ui.tk_helper import place
import ui.settings as s
import utils.database as db
from utils.models import make_tables
from utils.models import models_db_swap
from ui.tk_helper import change_button_color
import ui.language as en


def name_check(name):
    if len(name.split()) != 1:
        return False
    return True

def format_tag_info() -> str:
    """Formats current loaded wiki's tag information"""
    pass

def format_db_info() -> str:
    """Formats s.WIKI_DB_INFO"""
    pass

class SettingsPage(tk.Frame):
    def __init__(self, parent, button, status):
        change_button_color(button)
        tk.Frame.__init__(self, parent)
        self.status = status
        self.filepath = ""
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=18)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.layout()
        self.labels()
        self.display()
        self.entries()
        self.buttons()

    def add_wiki(self, name, notes):
        if name_check(name):
            res = name.capitalize()
            db.create_profile(res, notes)
            s.WIKI_DB_INFO = db.read_json()
            self.errors["text"] = f"{en.SETT_ADD1} {res}"
            s.DEFAULT_DB = res
            self.loaded["text"] = res
            s.WIKI_LIST.append(res)
            self.swap["values"] = s.WIKI_LIST
            self.swap.set(res)
            self.status["text"] = res
            db.load_profile(res)
            s.DB_FILE = f"{res}.db"
            # Changing DB, making its tables
            s.DB.close()
            s.DB = SqliteDatabase(s.DB_FILE)
            s.DB.connect()
            models_db_swap()
            make_tables()
        else:
            self.errors["text"] = en.SETT_ERR1
        self.name_entry.delete(0, "end")
        self.notes_entry.delete(0, "end")

    def delete_wiki(self, name):
        res = f"{name}"
        if s.WIKI_DB_INFO["wikis"].get(res, "") != "":
            db.delete_profile(res)
        else:
            self.errors["text"] = f"{en.SETT_ERR2} {name}."

    def get_filepath(self):
        filename = askopenfilename()
        if filename == "":
            pass
        elif ".db" not in os.path.basename(filename):
            self.import_di.config(fg=s.BUTTON_R)
            self.import_di["text"] = en.SETT_ERR3
        # Test if actual db
        else:
            self.filepath = filename
            self.import_di.config(fg=s.SEARCHBG)
            self.import_di["text"] = filename
            self.import_button.config(bg=s.SEARCHBG)

    def labels(self):
        wiki_name = tk.Label(self.left, text=en.LAB_SETT1, bg=s.FG,
                             fg=s.TEXT1, font=(s.FONT1, 9))
        place(wiki_name, h=0.05, w=0.2, x=0, y=0)
        wiki_notes = tk.Label(self.left, text=en.LAB_SETT2, bg=s.FG,
                             fg=s.TEXT1, font=(s.FONT1, 9))
        place(wiki_notes, h=0.05, w=0.2, x=0, y=0.04)
        swap_name = tk.Label(self.left, text=en.LAB_SETT3, bg=s.FG,
                             fg=s.TEXT1, font=(s.FONT1, 9))
        place(swap_name, h=0.05, w=0.2, x=0, y=0.103)
        wiki_label = tk.Label(self.left, text=en.LAB_SETT4, bg=s.FG,
                              fg=s.TEXT1, font=(s.FONT1, 9))
        place(wiki_label, h=0.05, w=0.2, x=0, y=0.155)
        add_tag_label = tk.Label(self.left, text=en.LAB_SETT5, bg=s.FG,
                         fg=s.TEXT1, font=(s.FONT1, 9))
        place(add_tag_label, h=0.05, w=0.2, x=0, y=0.21)
        import_label = tk.Label(self.left, text=en.LAB_SETT6, bg=s.FG,
                                fg=s.TEXT1, font=(s.FONT1, 9))
        place(import_label, h=0.05, w=0.2, x=0, y=0.295)

    def entries(self):
        self.name_entry = tk.Entry(self.left, bg=s.SEARCHFG)
        place(self.name_entry, h="", w=0.3, x=0.25, y=0.01)
        self.notes_entry = tk.Entry(self.left, bg=s.SEARCHFG)
        place(self.notes_entry, h="", w=0.3, x=0.25, y=0.05)
        self.swap = ttk.Combobox(self.left, value=s.WIKI_LIST)
        self.swap["state"] = "readonly"
        self.swap.current(0)
        place(self.swap, h="", w=0.3, x=0.25, y=0.11)
        self.change_entry = tk.Entry(self.left, bg=s.SEARCHFG)
        place(self.change_entry, h="", w=0.3, x=0.25, y=0.165)
        self.add_tag_entry = tk.Entry(self.left, bg=s.SEARCHFG)
        place(self.add_tag_entry, h="", w=0.3, x=0.25, y=0.22)
        
    def buttons(self):
        add_button = tk.Button(self.left, text=en.SETT_B1, bg=s.SEARCHBG, fg=s.TEXT3,
                               command=lambda: self.add_wiki(self.name_entry.get(),
                               self.notes_entry.get()))
        place(add_button, h="", w=0.3, x=0.59, y=0.005)
        swap_button = tk.Button(self.left, text=en.SETT_B2, bg=s.SEARCHBG,
                                fg=s.TEXT3)
        place(swap_button, h="", w=0.3, x=0.59, y=0.106)
        edit_name_button = tk.Button(self.left, text=en.SETT_B3, bg=s.SEARCHBG,
                                  fg=s.TEXT3)
        place(edit_name_button, h="", w=0.18, x=0.59, y=0.16)
        edit_notes_button = tk.Button(self.left, text=en.SETT_B4, bg=s.SEARCHBG,
                                      fg=s.TEXT3)
        place(edit_notes_button, h="", w=0.18, x=0.79, y=0.16)
        import_select = tk.Button(self.left, text=en.SETT_B5, bg=s.SEARCHBG,
                                  fg=s.TEXT3, command=lambda: self.get_filepath())
        place(import_select, h="", w=0.3, x=0.25, y=0.3)
        self.import_button = tk.Button(self.left, text=en.SETT_B6, bg=s.BUTTON_R,
                                       fg=s.TEXT3)
        place(self.import_button, h="", w=0.3, x=0.59, y=0.3)
        self.add_tag_button = tk.Button(self.left, text=en.SETT_B7, bg=s.SEARCHBG,
                                        fg=s.TEXT3)
        place(self.add_tag_button, h="", w=0.3, x=0.59, y=0.215)
        del_button = tk.Button(self.left, text=en.SETT_B8, bg=s.BUTTON_R,
                               fg=s.TEXT3)
        place(del_button, h="", w=0.2, x=0.79, y=0.96)

    def display(self):
        """Anything related to information displaying."""
        self.info = tk.Label(self.right, bg=s.BG2, fg=s.SEARCHBG)
        place(self.info, h=0.92, w=1, x=0, y=0.08)
        self.errors = tk.Label(self.right, text="", anchor="w", bg=s.BG2,
                               fg=s.BUTTON_R, font=(s.NORMAL_FONT, 12, "bold"), padx=10)
        place(self.errors, h=0.08, w=1, x=0, y=0)
        self.import_di = tk.Label(self.left, bg=s.BG2, font=(s.NORMAL_FONT, 11),
                                  anchor="w", text="", padx=5)
        place(self.import_di, h=0.035, w=0.9, x=0.02, y=0.365)
        self.display_info()

    def display_info(self):
        load_info = tk.Label(self.info, text=en.SETT_DIS1, font=(
                          s.FONT1, 11), bg=s.BG2, fg=s.SEARCHBG, anchor="w")
        place(load_info, h=0.05, w=0.9, x=0.052, y=0)
        self.loaded = tk.Label(self.info, text=s.DEFAULT_DB, font=(s.FONT1, 20, "bold"),
                          bg=s.BG2, fg=s.SEARCHBG)
        place(self.loaded, h=0.08, w=0.9, x=0.052, y=0.04)
        basics = tk.Label(self.info)

    def layout(self):
        """All partitions are relative to self.content"""
        self.right = tk.Frame(self.content, bg=s.FG)
        place(self.right, h=1, w=0.5, x=0.5, y=0)
        self.left = tk.Frame(self.content, bg=s.FG)
        place(self.left, h=1, w=0.5, x=0, y=0)
