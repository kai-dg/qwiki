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
from ui.tk_helper import change_button_color
import ui.language as en
import ui.settings as s
import utils.globals as g
import utils.json_database as jdb
import utils.models as db


def name_check(name:str) -> bool:
    """Checks if name for database file is one word only."""
    if len(name.split()) != 1:
        return False
    return True

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

    def set_combobox(self):
        """Sets the dropbox menu on the label Load:"""
        self.swap.set(g.DEFAULT_DB)

    def set_loaded_display(self):
        """Refreshes searchbar's DB status and current loaded on right side 
        info display
        """
        self.loaded["text"] = g.DEFAULT_DB
        self.description["text"] = g.WIKI_DB_INFO["wikis"][g.DEFAULT_DB]
        self.status["text"] = g.DEFAULT_DB

    def add_wiki(self, name, notes):
        """Add Wiki's button function"""
        if name_check(name):
            res = name.capitalize()
            jdb.create_profile(res, notes)
            g.WIKI_DB_INFO = jdb.read_json()
            self.errors["text"] = f"{en.SETT_ADD1} {res}"
            g.DEFAULT_DB = res
            self.loaded["text"] = res
            self.description["text"] = notes
            g.WIKI_LIST.append(res)
            self.swap["values"] = g.WIKI_LIST
            self.swap.set(res)
            self.status["text"] = res
            jdb.change_profile(res)
            db.change_database(res)
            db.make_tables()
            g.MODELCTRL = db.set_ctrl()
            g.QUERY = db.set_query()
        else:
            self.errors["text"] = en.SETT_ERR1
        self.name_entry.delete(0, "end")
        self.notes_entry.delete(0, "end")

    def delete_wiki(self):
        """Delete Wiki button's function"""
        target = g.DEFAULT_DB
        db.delete_database()
        self.errors["text"] = f"{en.SETT_ERR2} {target}"
        self.set_loaded_display()
        self.swap.config(value=g.WIKI_LIST)
        self.set_combobox()
        g.MODELCTRL = db.set_ctrl()
        g.QUERY = db.set_query()

    def load_wiki(self):
        """Load button's function"""
        name = self.swap.get()
        jdb.change_profile(name)
        db.change_database(name)
        db.init_database_info()
        self.set_loaded_display()
        self.errors["text"] = f"{en.SETT_ERR4} {name}"
        self.set_combobox()
        g.MODELCTRL = db.set_ctrl()
        g.QUERY = db.set_query()

    def update_wiki_name(self):
        """Edit label: Name button's function"""
        old = f"{g.DB_FILE}"
        name = self.change_entry.get().title()
        check = name_check(name)
        if check:
            filename = f"{name}.db"
            db.rename_database(filename)
            db.change_database(name)
            jdb.update_profile_name(name)
            g.DEFAULT_DB = name
            db.init_database_info()
            self.set_loaded_display()
            self.errors["text"] = f"{en.SETT_ERR5} {old.replace('.db', '')} to {name}"
            g.MODELCTRL = db.set_ctrl()
            g.QUERY = db.set_query()
        else:
            self.errors["text"] = en.SETT_ERR1

    def update_wiki_desc(self):
        """Label Edit: Button Desc. function"""
        desc = self.change_entry.get()
        jdb.update_profile_desc(desc)
        self.set_loaded_display()

    def get_filepath(self):
        """Label Import: Button Browse... function"""
        filename = askopenfilename()
        if filename == "":
            pass
        elif ".db" not in os.path.basename(filename):
            self.import_display.config(fg=s.BUTTON_R)
            self.import_display["text"] = en.SETT_ERR3
            # Test if actual db
        else:
            self.filepath = filename
            self.import_display.config(fg=s.SEARCHBG)
            self.import_display["text"] = filename
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
        self.swap = ttk.Combobox(self.left, value=g.WIKI_LIST)
        self.swap["state"] = "readonly"
        self.set_combobox()
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
                                fg=s.TEXT3, command=lambda: self.load_wiki())
        place(swap_button, h="", w=0.3, x=0.59, y=0.106)
        edit_name_button = tk.Button(self.left, text=en.SETT_B3, bg=s.SEARCHBG,
                                  fg=s.TEXT3, command=lambda: self.update_wiki_name())
        place(edit_name_button, h="", w=0.18, x=0.59, y=0.16)
        edit_notes_button = tk.Button(self.left, text=en.SETT_B4, bg=s.SEARCHBG,
                                      fg=s.TEXT3, command=lambda: self.update_wiki_desc())
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
                               fg=s.TEXT3, command=lambda: self.delete_wiki())
        place(del_button, h="", w=0.2, x=0.79, y=0.96)

    def display(self):
        """Anything related to information displaying."""
        self.info = tk.Label(self.right, bg=s.BG2, fg=s.SEARCHBG)
        place(self.info, h=0.92, w=1, x=0, y=0.08)
        self.errors = tk.Label(self.right, text="", anchor="w", bg=s.BG2,
                               fg=s.BUTTON_R, font=(s.FONT2, 12, "bold"), padx=10)
        place(self.errors, h=0.08, w=1, x=0, y=0)
        self.import_display = tk.Label(self.left, bg=s.BG2, font=(s.FONT2, 11),
                                  anchor="w", text="", padx=5)
        place(self.import_display, h=0.035, w=0.9, x=0.02, y=0.365)
        self.display_info()

    def display_info(self):
        load_info = tk.Label(self.info, text=en.SETT_DIS1, font=(
                          s.FONT1, 11), bg=s.BG2, fg=s.SEARCHBG, anchor="w")
        place(load_info, h=0.05, w=0.9, x=0.052, y=0)
        self.loaded = tk.Label(self.info, text=g.DEFAULT_DB, font=(s.FONT1, 20, "bold"),
                          bg=s.BG2, fg=s.SEARCHBG, anchor="w")
        place(self.loaded, h=0.08, w=0.9, x=0.052, y=0.04)
        self.description = tk.Label(self.info, text=g.WIKI_DB_INFO["wikis"][g.DEFAULT_DB],
                                    font=(s.FONT1, 11), anchor="w", bg=s.BG2, fg=s.SEARCHBG)
        place(self.description, h=0.04, w=0.9, x=0.052, y=0.1)
        page_amt = f"{en.SETT_DIS2} {g.QUERY.page_amt_stats()}"
        tag_amt = f"{en.SETT_DIS3}"
        self.loaded_stats = tk.Label(self.info, text=page_amt, bg=s.BG2, fg=s.SEARCHBG,
                                     anchor="w", font=(s.FONT1, 11))
        place(self.loaded_stats, h=0.04, w=0.4, x=0.052, y=0.17)

    def layout(self):
        """All partitions are relative to self.content"""
        self.right = tk.Frame(self.content, bg=s.FG)
        place(self.right, h=1, w=0.5, x=0.5, y=0)
        self.left = tk.Frame(self.content, bg=s.FG)
        place(self.left, h=1, w=0.5, x=0, y=0)
