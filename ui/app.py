#!/usr/bin/env python3
"""Entry point for Tkinter's app loop"""
from peewee import *
import tkinter as tk
import ui.settings as s
import utils.globals as g
import utils.json_database as jdb # Need this to prevent circular import
from ui.tk_helper import place
from ui.tk_helper import refresh_globals
import ui.language as en
from ui.page_wiki import WikiPage
from ui.page_change_wiki import SettingsPage
from ui.page_add import AddPage
from ui.page_update import UpdatePage
from ui.page_delete import DelPage
from ui.page_help import HelpPage
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
        self.frame = tk.Frame(self.root, bg=s.FG)
        place(self.frame, h=1, w=1, x=0.5, y=0.5, a="c")
        self.fuzz_bar_active = False
        self.search_term = ""
        self.static_bottom_buttons()
        self.initial_frame()
        self.searchbar_display()
        db.init_database_info()
        self.root.mainloop()
        g.DB.close()

    def replace(self, cls):
        """Controller for changing self.content frame. Deletes current frame
        to wipe the non init tk objects from that page.
        """
        self.content.destroy()

    def initial_frame(self):
        """Initial screen when starting the app"""
        self.content = tk.Frame(self.frame, bg=s.FG)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        self.replace(HelpPage(self.frame, "help"))

    def fuzzy_frame(self):
        self.fuzz_bar = tk.Listbox(self.root, selectmode="multiple", height=1,
                                   font=(15))
        place(self.fuzz_bar, h="", w=0.6, x=0.2, y=0.04)
        self.fuzz_bar.bind("<<ListboxSelect>>", self.fuzzy_query)
        self.fuzz_bar.place_forget()

    def fuzzy_on_off(self, event):
        if self.fuzz_bar_active:
            self.fuzz_bar.place_forget()
            self.fuzz_bar.delete(0, "end")

    def fuzzy_searchbar(self, event):
        self.search_term = self.searchbar.get()
        if self.search_term != "":
            self.fuzz_bar.delete(0, "end")
            suggestions = g.QUERY.fuzzy_page_match(self.search_term)
            self.fuzz_bar.config(height=len(suggestions))
            for item in suggestions:
                self.fuzz_bar.insert("end", item.name)  
            self.fuzz_bar_active = True
            place(self.fuzz_bar, h="", w=0.6, x=0.2, y=0.04)
        else:
            self.fuzz_bar.place_forget()
            self.fuzz_bar.delete(0, "end")
        self.searchbar.focus()

    def fuzzy_query(self, query):
        name = query.widget.get(query.widget.curselection())
        self.replace(WikiPage(self.frame, name))
        self.fuzz_bar_active = False
        self.fuzz_bar.destroy()
        self.fuzzy_frame()
        self.frame.focus()

    def searchbar_display(self):
        """Everything in the top section (search bar and buttons)."""
        self.frame_search = tk.Frame(self.frame, bg=s.SEARCHBG)
        place(self.frame_search, h=0.04, w=2, x=0.1, y=0, a="n")
        self.searchlabel = tk.Label(self.frame_search, text=g.DEFAULT_DB, bg=s.SEARCHBG,
                                     font=(s.FONT1, 9, "bold"), anchor="center")
        place(self.searchlabel, h=1, w=0.1, x=0.45, y=0)
        self.searchbar = tk.Entry(self.frame_search, font=(s.FONT2, 12), bg=s.SEARCHFG,
                                  fg=s.TEXT2, borderwidth=8, relief="flat")
        self.searchbar.bind('<KeyRelease>', self.fuzzy_searchbar)
        self.searchbar.bind("<Return>", (lambda event: self.replace(
                            WikiPage(self.frame, self.searchbar.get()))))
        place(self.searchbar, h=1, w=0.3, x=0.55, y=0)
        searchbutton = tk.Button(self.frame_search, text=en.SEARCH_B1, font=(s.FONT2, 9),
                                 bg=s.BUTTON_D, fg=s.TEXT1, activebackground=s.BUTTON_A,
                                 activeforeground=s.TEXT2,
                                 command=lambda: self.replace(WikiPage(self.frame,
                                 self.searchbar.get())))
        place(searchbutton, h=1, w=0.05, x=0.85, y=0)
        search_by_tag = tk.Button(self.frame_search, text=en.SEARCH_B2, font=(s.FONT2, 9),
                                 bg=s.BUTTON_D, fg=s.TEXT1, activebackground=s.BUTTON_A,
                                 activeforeground=s.TEXT2)
        place(search_by_tag, h=1, w=0.05, x=0.90, y=0)
        self.fuzzy_frame()

    def static_bottom_buttons(self):
        """Everything on the bottom section (the row of buttons)."""
        self.frame_editor = tk.Frame(self.frame, bg="red")
        place(self.frame_editor, h=0.03, w=1, x=0.5, y=1, a="s")
        self.add_wiki = tk.Button(self.frame_editor, text=en.BOTT_B1, font=(s.FONT1, 10,
                                  "bold"), bg=s.SEARCHBG, fg=s.TEXT3,
                                  command=lambda: self.replace(AddPage(self.frame, "add")))
        place(self.add_wiki, h=1, w=0.2, x=0, y=0)
        self.update_wiki = tk.Button(self.frame_editor, text=en.BOTT_B2, font=(s.FONT1,
                                     10, "bold"), bg=s.SEARCHBG, fg=s.TEXT3,
                                     command=lambda: self.replace(UpdatePage(self.frame, "update")))
        place(self.update_wiki, h=1, w=0.2, x=0.2, y=0)
        self.delete_wiki = tk.Button(self.frame_editor, text=en.BOTT_B3, font=(
                                     s.FONT1, 10, "bold"), bg=s.SEARCHBG, fg=s.TEXT3,
                                     command=lambda: self.replace(DelPage(
                                     self.frame, "del")))
        place(self.delete_wiki, h=1, w=0.2, x=0.4, y=0)
        self.sett_wiki = tk.Button(self.frame_editor, text=en.BOTT_B4, font=(
                                   s.FONT1, 10, "bold"), bg=s.SEARCHBG, fg=s.TEXT3,
                                    command=lambda: [self.replace(SettingsPage(self.frame, "sett",
                                    self.searchlabel)), refresh_globals()])
        place(self.sett_wiki, h=1, w=0.2, x=0.6, y=0)
        self.help_wiki = tk.Button(self.frame_editor, text=en.BOTT_B5, font=(s.FONT1,
                                   10, "bold"), bg=s.SEARCHBG, fg=s.TEXT3,
                                   command=lambda: [self.replace(HelpPage(self.frame,
                                   "help")), refresh_globals()])
        place(self.help_wiki, h=1, w=0.2, x=0.8, y=0)
        # Globals for changing button colors when pressed
        g.MENU_BUTTONS = {
            "add": self.add_wiki,
            "update": self.update_wiki,
            "sett": self.sett_wiki,
            "help": self.help_wiki,
            "del": self.delete_wiki
        }
