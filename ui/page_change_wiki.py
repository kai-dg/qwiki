#!/usr/bin/env python3
"""Add page button frame"""
import tkinter as tk
from tkinter import ttk
from ui.tk_helper import place
import ui.settings as s
import utils.database as db


def name_check(name):
    if len(name.split()) != 1:
        return False
    return True

class ChangeWikiPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=18)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.layout()
        self.labels()
        self.display()
        self.entries()
        self.buttons()
        self.display()

    def add_wiki(self, name, notes):
        if name_check(name):
            res = f"{name.capitalize()}.db"
            db.create_profile(res, notes)
            self.errors["text"] = f"Added new wiki: {res}"
            s.WIKI_LIST.append(res)
            self.swap["values"] = s.WIKI_LIST
            self.swap.set(res)
        else:
            self.errors["text"] = "Please enter a 1 word name only."

    def labels(self):
        swap_name = tk.Label(self.left, text="Loaded:", bg=s.FG,
                             fg=s.TEXT1, font=(s.FONT1, 9))
        place(swap_name, h=0.05, w=0.2, x=0, y=0)
        wiki_name = tk.Label(self.left, text="Wiki Name:", bg=s.FG,
                             fg=s.TEXT1, font=(s.FONT1, 9))
        place(wiki_name, h=0.05, w=0.2, x=0, y=0.1)
        wiki_notes = tk.Label(self.left, text="Desc.:", bg=s.FG,
                             fg=s.TEXT1, font=(s.FONT1, 9))
        place(wiki_notes, h=0.05, w=0.2, x=0, y=0.15)
        wiki_label = tk.Label(self.left, text="Edit Wiki:", bg=s.FG,
                              fg=s.TEXT1, font=(s.FONT1, 9))
        place(wiki_label, h=0.05, w=0.2, x=0, y=0.25)
        import_label = tk.Label(self.left, text="Import:", bg=s.FG,
                                fg=s.TEXT1, font=(s.FONT1, 9))
        place(import_label, h=0.05, w=0.2, x=0, y=0.35)

    def entries(self):
        self.swap = ttk.Combobox(self.left, value=s.WIKI_LIST)
        self.swap.current(0)
        place(self.swap, h="", w=0.3, x=0.25, y=0.01)
        self.name_entry = tk.Entry(self.left, bg=s.SEARCHFG)
        place(self.name_entry, h="", w=0.3, x=0.25, y=0.11)
        self.notes_entry = tk.Entry(self.left, bg=s.SEARCHFG)
        place(self.notes_entry, h="", w=0.3, x=0.25, y=0.16)
        self.change_entry = tk.Entry(self.left) # dropdown
        place(self.change_entry, h="", w=0.3, x=0.25, y=0.26)
        self.import_entry = tk.Entry(self.left)
        place(self.import_entry, h="", w=0.3, x=0.25, y=0.36)
        
    def buttons(self):
        swap_button = tk.Button(self.left, text="Change", bg=s.SEARCHBG,
                                fg=s.TEXT3)
        place(swap_button, h="", w=0.3, x=0.59, y=0.005)
        add_button = tk.Button(self.left, text="Add", bg=s.SEARCHBG, fg=s.TEXT3,
                               command=lambda: self.add_wiki(self.name_entry.get(),
                               self.notes_entry.get()))
        place(add_button, h="", w=0.18, x=0.59, y=0.105)
        del_button = tk.Button(self.left, text="Delete", bg=s.SEARCHBG,
                               fg=s.TEXT3)
        place(del_button, h="", w=0.18, x=0.79, y=0.105)
        edit_name_button = tk.Button(self.left, text="Name", bg=s.SEARCHBG,
                                  fg=s.TEXT3)
        place(edit_name_button, h="", w=0.18, x=0.59, y=0.255)
        edit_notes_button = tk.Button(self.left, text="Desc.", bg=s.SEARCHBG,
                                      fg=s.TEXT3)
        place(edit_notes_button, h="", w=0.18, x=0.79, y=0.255)
        import_button = tk.Button(self.left, text="Import", bg=s.SEARCHBG,
                                  fg=s.TEXT3)
        place(import_button, h="", w=0.3, x=0.59, y=0.355)

    def display(self):
        self.info = tk.Label(self.right, bg=s.BG2, fg=s.SEARCHBG)
        place(self.info, h=1, w=1, x=0, y=0)
        self.errors = tk.Label(self.left, text="", anchor="w", bg=s.FG,
                               fg=s.TEXT1, font=(s.NORMAL_FONT, 12, "bold"))
        place(self.errors, h=0.08, w=1, x=0, y=0.4)

    def layout(self):
        """All partitions are relative to self.content"""
        self.right = tk.Frame(self.content, bg="black")
        place(self.right, h=1, w=0.5, x=0.5, y=0)
        self.left = tk.Frame(self.content, bg=s.FG)
        place(self.left, h=1, w=0.5, x=0, y=0)
