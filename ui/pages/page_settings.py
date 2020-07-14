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
from ui.tk_styles import SettingsPageStyles
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
    def __init__(self, parent, button):
        change_button_color(button)
        tk.Frame.__init__(self, parent)
        self.base_f = tk.Frame(None)
        place(self.base_f, h=0.93, w=1, x=0, y=0.04)
        self.filepath = ""
        self.layout()
        self.labels()
        self.display()
        self.entries()
        self.buttons()
        self.styles = SettingsPageStyles(self)

    def set_combobox(self):
        """Sets the dropbox menu on the label Load:"""
        self.swap.set(g.DEFAULT_DB)

    def set_loaded_display(self):
        """Refreshes searchbar's DB status and current loaded on right side 
        info display
        """
        self.loaded_name_l["text"] = g.DEFAULT_DB
        self.desc_l["text"] = g.WIKI_DB_INFO["wikis"][g.DEFAULT_DB]
        g.DB_STATUS["text"] = g.DEFAULT_DB

    def add_wiki(self, name, notes):
        """Add Wiki's button function"""
        if name_check(name):
            res = name.capitalize()
            jdb.create_profile(res, notes)
            g.WIKI_DB_INFO = jdb.read_json()
            self.errs_l["text"] = f"{en.SETT_ADD1} {res}"
            g.DEFAULT_DB = res
            self.loaded_name_l["text"] = res
            self.desc_l["text"] = notes
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
            self.errs_l["text"] = en.SETT_ERR1
        self.name_e.delete(0, "end")
        self.notes_e.delete(0, "end")

    def delete_wiki(self):
        """Delete Wiki button's function"""
        target = g.DEFAULT_DB
        db.delete_database()
        self.errs_l["text"] = f"{en.SETT_ERR2} {target}"
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
        self.errs_l["text"] = f"{en.SETT_ERR4} {name}"
        self.set_combobox()
        g.MODELCTRL = db.set_ctrl()
        g.QUERY = db.set_query()

    def update_wiki_name(self):
        """Edit label: Name button's function"""
        old = f"{g.DB_FILE}"
        name = self.edit_e.get().title()
        check = name_check(name)
        if check:
            filename = f"{name}.db"
            db.rename_database(filename)
            db.change_database(name)
            jdb.update_profile_name(name)
            g.DEFAULT_DB = name
            db.init_database_info()
            self.set_loaded_display()
            self.errs_l["text"] = f"{en.SETT_ERR5} {old.replace('.db', '')} to {name}"
            g.MODELCTRL = db.set_ctrl()
            g.QUERY = db.set_query()
        else:
            self.errs_l["text"] = en.SETT_ERR1

    def update_wiki_desc(self):
        """Label Edit: Button Desc. function"""
        desc = self.edit_e.get()
        jdb.update_profile_desc(desc)
        self.set_loaded_display()

    def get_filepath(self):
        """Label Import: Button Browse... function
        TODO: Check if basefile name already exists in profile
        """
        filename = askopenfilename()
        if filename == "":
            pass
        elif ".db" not in os.path.basename(filename):
            self.info_imp_l.config(fg=s.BUTTON_R)
            self.info_imp_l["text"] = en.SETT_ERR3
            # Test if actual db
        else:
            self.filepath = filename
            self.info_imp_l.config(fg=s.SEARCHBG)
            self.info_imp_l["text"] = filename
            self.import_b.config(bg=s.SEARCHBG)

    def import_wiki(self):
        if self.filepath != "":
            db.import_database(self.filepath)
            self.set_loaded_display()

    def labels(self):
        self.name_l = tk.Label(self.left_f)
        place(self.name_l, h=0.05, w=0.2, x=0, y=0)
        self.notes_l = tk.Label(self.left_f)
        place(self.notes_l, h=0.05, w=0.2, x=0, y=0.04)
        self.load_l = tk.Label(self.left_f)
        place(self.load_l, h=0.05, w=0.2, x=0, y=0.103)
        self.edit_l = tk.Label(self.left_f)
        place(self.edit_l, h=0.05, w=0.2, x=0, y=0.155)
        self.tag_l = tk.Label(self.left_f)
        place(self.tag_l, h=0.05, w=0.2, x=0, y=0.21)
        self.import_l = tk.Label(self.left_f)
        place(self.import_l, h=0.05, w=0.2, x=0, y=0.295)

    def entries(self):
        self.name_e = tk.Entry(self.left_f)
        place(self.name_e, h="", w=0.3, x=0.25, y=0.01)
        self.notes_e = tk.Entry(self.left_f)
        place(self.notes_e, h="", w=0.3, x=0.25, y=0.05)
        self.swap = ttk.Combobox(self.left_f, value=g.WIKI_LIST)
        self.swap["state"] = "readonly"
        self.set_combobox()
        place(self.swap, h="", w=0.3, x=0.25, y=0.11)
        self.edit_e = tk.Entry(self.left_f)
        place(self.edit_e, h="", w=0.3, x=0.25, y=0.165)
        self.tag_e = tk.Entry(self.left_f)
        place(self.tag_e, h="", w=0.3, x=0.25, y=0.22)
        
    def buttons(self):
        self.add_wiki_b = tk.Button(self.left_f, command=lambda: self.add_wiki(
                                    self.name_e.get(), self.notes_e.get()))
        place(self.add_wiki_b, h="", w=0.3, x=0.59, y=0.005)
        self.load_b = tk.Button(self.left_f, command=lambda: self.load_wiki())
        place(self.load_b, h="", w=0.3, x=0.59, y=0.106)
        self.edit_name_b = tk.Button(self.left_f, command=lambda:
                                     self.update_wiki_name())
        place(self.edit_name_b, h="", w=0.18, x=0.59, y=0.16)
        self.edit_notes_b = tk.Button(self.left_f, command=lambda:
                                      self.update_wiki_desc())
        place(self.edit_notes_b, h="", w=0.18, x=0.79, y=0.16)
        self.browse_b = tk.Button(self.left_f, command=lambda: self.get_filepath())
        place(self.browse_b, h="", w=0.3, x=0.25, y=0.3)
        self.import_b = tk.Button(self.left_f, command=lambda: self.import_wiki())
        place(self.import_b, h="", w=0.3, x=0.59, y=0.3)
        self.tag_b = tk.Button(self.left_f)
        place(self.tag_b, h="", w=0.3, x=0.59, y=0.215)
        self.del_b = tk.Button(self.left_f, command=lambda: self.delete_wiki())
        place(self.del_b, h="", w=0.2, x=0.79, y=0.96)

    def display(self):
        """Anything related to information displaying."""
        self.info_l = tk.Label(self.right_f)
        place(self.info_l, h=0.92, w=1, x=0, y=0.08)
        self.errs_l = tk.Label(self.right_f)
        place(self.errs_l, h=0.08, w=1, x=0, y=0)
        self.info_imp_l = tk.Label(self.left_f)
        place(self.info_imp_l, h=0.035, w=0.9, x=0.02, y=0.365)
        self.display_info()

    def display_info(self):
        self.loaded_l = tk.Label(self.info_l)
        place(self.loaded_l, h=0.05, w=0.9, x=0.052, y=0)
        self.loaded_name_l = tk.Label(self.info_l)
        place(self.loaded_name_l, h=0.08, w=0.9, x=0.052, y=0.04)
        self.desc_l = tk.Label(self.info_l)
        place(self.desc_l, h=0.04, w=0.9, x=0.052, y=0.1)
        page_amt = f"{en.SETT_DIS2} {g.QUERY.page_amt_stats()}"
        tag_amt = f"{en.SETT_DIS3}"
        self.loaded_stats_l = tk.Label(self.info_l, text=page_amt)
        place(self.loaded_stats_l, h=0.04, w=0.4, x=0.052, y=0.17)

    def layout(self):
        """All partitions are relative to self.content"""
        self.right_f = tk.Frame(self.base_f, bg=s.FG)
        place(self.right_f, h=1, w=0.5, x=0.5, y=0)
        self.left_f = tk.Frame(self.base_f, bg=s.FG)
        place(self.left_f, h=1, w=0.5, x=0, y=0)
