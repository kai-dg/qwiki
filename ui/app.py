#!/usr/bin/env python3
"""Entry point for Tkinter's app loop"""
from peewee import *
import tkinter as tk
import ui.settings as s
import utils.globals as g
import utils.json_database as jdb # Need this to prevent circular import
import ui.tk_helper as tkh
from ui.tk_styles import AppStyles
import ui.language as en
from ui.pages.page_wiki import WikiPage
from ui.pages.page_settings import SettingsPage
from ui.pages.page_add import AddPage
from ui.pages.page_update import UpdatePage
from ui.pages.page_delete import DelPage
from ui.pages.page_help import HelpPage
from ui.image_window import ImageWindow
import utils.models as db
g.MODELCTRL = db.set_ctrl()
g.QUERY = db.set_query()
g.IMAGE_WINDOW = ImageWindow


class App():
    """Every button on the static interface should use self.replace() to
    change frames.
    """
    def __init__(self):
        self.root = tk.Tk()
        g.ROOT = self.root
        self.root.title(s.TITLE)
        self.root.geometry(f"{s.W_HEIGHT}x{s.W_WIDTH}")
        self.root.minsize(s.W_HEIGHT, s.W_WIDTH)
        self.root.bind("<Button-1>", self.fuzzy_on_off)
        self.frame = tk.Frame(self.root, bg=s.FG)
        tkh.place(self.frame, h=1, w=1, x=0, y=0)
        self.fuzz_bar_active = False
        self.search_term = ""
        self.create_menu_buttons()
        self.create_initial_frame()
        self.create_searchbar()
        db.init_database_info()
        self.styles = AppStyles(self)
        tkh.change_button_color("help") # Initial page
        self.root.mainloop()
        g.DB.close()

    def set_query(self):
        """Format the entry for a query and set it as global"""
        g.TARGET = self.search_e.get().rstrip().title()

    def replace(self, cls, button):
        """Controller for changing self.content frame. Deletes current frame
        to wipe the non init tk objects from that page.
        """
        self.content.destroy()
        self.content = tk.Frame(self.frame)
        tkh.place(self.content, h=0.93, w=1, x=0, y=0.04, a="n")
        cls(self.content, button)

    def create_initial_frame(self):
        """Initial screen when starting the app"""
        self.content = tk.Frame(self.frame)
        tkh.place(self.content, h=0.93, w=1, x=0, y=0.04, a="n")
        self.replace(HelpPage, "help")

    def fuzzy_frame(self):
        self.fuzz_list = tk.Listbox(self.root)
        tkh.place(self.fuzz_list, h="", w=0.6, x=0.2, y=0.04)
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
            tkh.place(self.fuzz_list, h="", w=0.6, x=0.2, y=0.04)
        else:
            self.fuzz_list.place_forget()
            self.fuzz_list.delete(0, "end")
        self.search_e.focus()

    def fuzzy_query(self, query):
        g.TARGET = query.widget.get(query.widget.curselection())
        self.replace(WikiPage, "")
        self.fuzz_bar_active = False
        self.fuzz_list.destroy()
        self.fuzzy_frame()
        self.frame.focus()

    def create_searchbar(self):
        """Everything in the top section (search bar and buttons)."""
        self.search_f = tk.Frame(self.frame)
        tkh.place(self.search_f, h=0.04, w=2, x=0.1, y=0, a="n")
        g.DB_STATUS = tk.Label(self.search_f)
        tkh.place(g.DB_STATUS, h=1, w=0.1, x=0.45, y=0)
        self.search_e = tk.Entry(self.search_f)
        self.search_e.bind('<KeyRelease>', self.fuzzy_searchbar)
        self.search_e.bind("<Return>", (lambda event: [self.set_query(),
                            self.replace(WikiPage, ""), self.fuzz_list.
                            place_forget(), self.frame.focus()]))
        tkh.place(self.search_e, h=1, w=0.3, x=0.55, y=0)
        self.search_b = tk.Button(self.search_f, command=lambda: [self.
                                  set_query(), self.replace(WikiPage, "")])
        tkh.place(self.search_b, h=1, w=0.05, x=0.85, y=0)
        self.search_tag_b = tk.Button(self.search_f, command=lambda: ImageWindow())
        tkh.place(self.search_tag_b, h=1, w=0.05, x=0.90, y=0)
        self.fuzzy_frame() # Autocomplete popup

    def create_menu_buttons(self):
        """Everything on the bottom section (the row of buttons)."""
        self.menu_f = tk.Frame(self.frame)
        tkh.place(self.menu_f, h=0.03, w=1, x=0.5, y=1, a="s")
        self.menu_add_b = tk.Button(self.menu_f, command=lambda: self.replace(
                                    AddPage, "add"))
        tkh.place(self.menu_add_b, h=1, w=0.2, x=0, y=0)
        self.menu_update_b = tk.Button(self.menu_f, command=lambda: self.replace(
                                       UpdatePage, "update"))
        tkh.place(self.menu_update_b, h=1, w=0.2, x=0.2, y=0)
        self.menu_del_b = tk.Button(self.menu_f, command=lambda: self.replace(
                                    DelPage, "del"))
        tkh.place(self.menu_del_b, h=1, w=0.2, x=0.4, y=0)
        self.menu_sett_b = tk.Button(self.menu_f, command=lambda: [self.replace(
                                     SettingsPage, "sett"), tkh.refresh_globals()])
        tkh.place(self.menu_sett_b, h=1, w=0.2, x=0.6, y=0)
        self.menu_help_b = tk.Button(self.menu_f, command=lambda: [self.replace(
                                     HelpPage, "help"), tkh.refresh_globals()])
        tkh.place(self.menu_help_b, h=1, w=0.2, x=0.8, y=0)
        # Globals for changing button colors when pressed
        g.MENU_BUTTONS = {
            "add": self.menu_add_b,
            "update": self.menu_update_b,
            "sett": self.menu_sett_b,
            "help": self.menu_help_b,
            "del": self.menu_del_b
        }
