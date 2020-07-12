#!/usr/bin/env python3
"""Entry point for Tkinter's app loop"""
from peewee import *
import tkinter as tk
import ui.settings as s
import utils.globals as g
import utils.json_database as jdb # Need this to prevent circular import
from ui.tk_helper import place
from ui.tk_helper import refresh_globals
from ui.tk_styles import AppStyles
import ui.language as en
from ui.pages.page_wiki import WikiPage
from ui.pages.page_settings import SettingsPage
from ui.pages.page_add import AddPage
from ui.pages.page_update import UpdatePage
from ui.pages.page_delete import DelPage
from ui.pages.page_help import HelpPage
import utils.models as db
g.MODELCTRL = db.set_ctrl()
g.QUERY = db.set_query()


class App():
    """Every button on the static interface should use self.replace() to
    change frames. Anything with static_ means any widget created in those functions
    will stay on the screen for the entire time.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(s.TITLE)
        self.root.geometry(f"{s.W_HEIGHT}x{s.W_WIDTH}")
        self.root.bind("<Button-1>", self.fuzzy_on_off)
        self.frame = tk.Frame(self.root)
        place(self.frame, h=1, w=1, x=0.5, y=0.5, a="c")
        self.fuzz_bar_active = False
        self.search_term = ""
        self.create_menu_buttons()
        self.create_initial_frame()
        self.create_searchbar()
        db.init_database_info()
        self.styles = AppStyles(self)
        self.root.mainloop()
        g.DB.close()

    def replace(self, cls):
        """Controller for changing self.content frame. Deletes current frame
        to wipe the non init tk objects from that page.
        """
        self.content.destroy()

    def create_initial_frame(self):
        """Initial screen when starting the app"""
        self.content = tk.Frame(self.frame)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.replace(HelpPage(self.frame, "help"))

    def fuzzy_frame(self):
        self.fuzz_list = tk.Listbox(self.root)
        place(self.fuzz_list, h="", w=0.6, x=0.2, y=0.04)
        self.fuzz_list.bind("<<ListboxSelect>>", self.fuzzy_query)
        self.fuzz_list.place_forget()

    def fuzzy_on_off(self, event):
        if self.fuzz_bar_active:
            self.fuzz_list.place_forget()
            self.fuzz_list.delete(0, "end")

    def fuzzy_searchbar(self, event):
        self.search_term = self.search_e.get()
        if self.search_term != "":
            self.fuzz_list.delete(0, "end")
            suggestions = g.QUERY.fuzzy_page_match(self.search_term,
                                                   s.SEARCHBAR_PG_LIMIT)
            self.fuzz_list.config(height=len(suggestions))
            for item in suggestions:
                self.fuzz_list.insert("end", item.name)  
            self.fuzz_bar_active = True
            place(self.fuzz_list, h="", w=0.6, x=0.2, y=0.04)
        else:
            self.fuzz_list.place_forget()
            self.fuzz_list.delete(0, "end")
        self.search_e.focus()

    def fuzzy_query(self, query):
        name = query.widget.get(query.widget.curselection())
        self.replace(WikiPage(self.frame, name))
        self.fuzz_bar_active = False
        self.fuzz_list.destroy()
        self.fuzzy_frame()
        self.frame.focus()

    def create_searchbar(self):
        """Everything in the top section (search bar and buttons)."""
        self.search_f = tk.Frame(self.frame)
        place(self.search_f, h=0.04, w=2, x=0.1, y=0, a="n")
        self.search_l = tk.Label(self.search_f)
        place(self.search_l, h=1, w=0.1, x=0.45, y=0)
        self.search_e = tk.Entry(self.search_f)
        self.search_e.bind('<KeyRelease>', self.fuzzy_searchbar)
        self.search_e.bind("<Return>", (lambda event: [self.replace(
                            WikiPage(self.frame, self.search_e.get())),
                            self.fuzz_list.place_forget(), self.frame.focus()]))
        place(self.search_e, h=1, w=0.3, x=0.55, y=0)
        self.search_b = tk.Button(self.search_f, command=lambda: self.replace(
                                  WikiPage(self.frame, self.search_e.get())))
        place(self.search_b, h=1, w=0.05, x=0.85, y=0)
        self.search_tag_b = tk.Button(self.search_f)
        place(self.search_tag_b, h=1, w=0.05, x=0.90, y=0)
        self.fuzzy_frame() # Autocomplete popup

    def create_menu_buttons(self):
        """Everything on the bottom section (the row of buttons)."""
        self.menu_f = tk.Frame(self.frame)
        place(self.menu_f, h=0.03, w=1, x=0.5, y=1, a="s")
        self.menu_add_b = tk.Button(self.menu_f, command=lambda: self.replace(
                                    AddPage(self.frame, "add")))
        place(self.menu_add_b, h=1, w=0.2, x=0, y=0)
        self.menu_update_b = tk.Button(self.menu_f, command=lambda: self.replace(
                                       UpdatePage(self.frame, "update")))
        place(self.menu_update_b, h=1, w=0.2, x=0.2, y=0)
        self.menu_del_b = tk.Button(self.menu_f, command=lambda: self.replace(
                                    DelPage(self.frame, "del")))
        place(self.menu_del_b, h=1, w=0.2, x=0.4, y=0)
        self.menu_sett_b = tk.Button(self.menu_f, command=lambda: [self.replace(
                                     SettingsPage(self.frame, "sett", self.search_l)),
                                     refresh_globals()])
        place(self.menu_sett_b, h=1, w=0.2, x=0.6, y=0)
        self.menu_help_b = tk.Button(self.menu_f, command=lambda: [self.replace(
                                     HelpPage(self.frame, "help")), refresh_globals()])
        place(self.menu_help_b, h=1, w=0.2, x=0.8, y=0)
        # Globals for changing button colors when pressed
        g.MENU_BUTTONS = {
            "add": self.menu_add_b,
            "update": self.menu_update_b,
            "sett": self.menu_sett_b,
            "help": self.menu_help_b,
            "del": self.menu_del_b
        }
