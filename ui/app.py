#!/usr/bin/env python3
from peewee import *
import tkinter as tk
import ui.settings as s
import utils.database as db
from ui.tk_helper import place
from ui.page_wiki import WikiPage
from ui.page_change_wiki import SettingsPage
from ui.page_add import AddPage
from ui.page_update import UpdatePage
from ui.page_confirms import DelConfirmPage
from ui.page_help import HelpPage
from utils.models import models_db_swap
s.WIKI_DB_INFO = db.read_json()
s.DEFAULT_DB = s.WIKI_DB_INFO["active"] if s.WIKI_DB_INFO["active"] != "" else s.DEFAULT_DB
s.DB_FILE = f"{s.DEFAULT_DB}.db"
models_db_swap()
s.WIKI_LIST = list(s.WIKI_DB_INFO["wikis"])
s.WIKI_LIST = [""] if s.WIKI_LIST == [] else s.WIKI_LIST


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(s.TITLE)
        self.root.geometry(f"{s.W_HEIGHT}x{s.W_WIDTH}")
        self.frame = tk.Frame(self.root, bg=s.FG)
        self.frame.place(relheight=1, relwidth=1, relx=0.5, rely=0.5, anchor="c")
        self.search_bar()
        self.bottom_buttons()
        self.content_f()
        self.root.mainloop()

    def button_color(self):
        pass

    def replace(self, cls):
        """Controller for changing self.content frame"""
        self.content.destroy()

    def content_f(self):
        self.content = tk.Frame(self.frame, bg=s.FG)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        self.replace(HelpPage(self.frame, "help"))

    def search_bar(self):
        frame_search = tk.Frame(self.frame, bg=s.SEARCHBG)
        place(frame_search, h=0.04, w=2, x=0.1, y=0, a="n")
        self.searchlabel = tk.Label(frame_search, text=s.DEFAULT_DB, bg=s.SEARCHBG,
                                     font=(s.FONT1, 9, "bold"), anchor="center")
        place(self.searchlabel, h=1, w=0.1, x=0.45, y=0)
        self.searchbar = tk.Entry(frame_search, font=(s.NORMAL_FONT, 12), bg=s.SEARCHFG,
                                  fg=s.TEXT2)
        place(self.searchbar, h=1, w=0.3, x=0.55, y=0)
        searchbutton = tk.Button(frame_search, text="SEARCH", font=(s.NORMAL_FONT, 9),
                                 bg=s.BUTTON_D, fg=s.TEXT1, activebackground=s.BUTTON_A,
                                 activeforeground=s.TEXT2,
                                 command=lambda: self.replace(WikiPage(self.frame,
                                 self.searchbar.get())))
        place(searchbutton, h=1, w=0.05, x=0.85, y=0)
        search_by_tag = tk.Button(frame_search, text="BY TAG", font=(s.NORMAL_FONT, 9),
                                 bg=s.BUTTON_D, fg=s.TEXT1, activebackground=s.BUTTON_A,
                                 activeforeground=s.TEXT2)
        place(search_by_tag, h=1, w=0.05, x=0.90, y=0)

    def bottom_buttons(self):
        self.frame_editor = tk.Frame(self.frame, bg="red")
        place(self.frame_editor, h=0.03, w=1, x=0.5, y=1, a="s")
        self.add_wiki = tk.Button(self.frame_editor, text="Add Page", font=(s.FONT1, 9, "bold"),
                                    bg=s.SEARCHBG, fg=s.TEXT3,
                             command=lambda: self.replace(AddPage(self.frame, "add")))
        place(self.add_wiki, h=1, w=0.2, x=0, y=0)
        self.update_wiki = tk.Button(self.frame_editor, text="Update Page", font=(s.FONT1, 9, "bold"),
                                    bg=s.SEARCHBG, fg=s.TEXT3,
                                command=lambda: self.replace(UpdatePage(self.frame, "update")))
        place(self.update_wiki, h=1, w=0.2, x=0.2, y=0)
        self.delete_wiki = tk.Button(self.frame_editor, text="Delete Page", font=(s.FONT1, 9, "bold"),
                                    bg=s.SEARCHBG, fg=s.TEXT3,
                                command=lambda: self.replace(DelConfirmPage(
                                self.frame)))
        place(self.delete_wiki, h=1, w=0.2, x=0.4, y=0)
        self.sett_wiki = tk.Button(self.frame_editor, text="Wiki Settings", font=(s.FONT1, 9, "bold"),
                                    bg=s.SEARCHBG, fg=s.TEXT3,
                                    command=lambda: self.replace(SettingsPage(self.frame, "sett",
                                    self.searchlabel)))
        place(self.sett_wiki, h=1, w=0.2, x=0.6, y=0)
        self.help_wiki = tk.Button(self.frame_editor, text="Help", font=(s.FONT1, 9, "bold"),
                                    bg=s.SEARCHBG, fg=s.TEXT3,
                                    command=lambda: self.replace(HelpPage(self.frame, "help")))
        place(self.help_wiki, h=1, w=0.2, x=0.8, y=0)
        s.MENU_BUTTONS = {
            "add": self.add_wiki,
            "update": self.update_wiki,
            "sett": self.sett_wiki,
            "help": self.help_wiki
        }

if __name__ == "__main__":
    pass
