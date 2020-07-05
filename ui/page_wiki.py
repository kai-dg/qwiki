#!/usr/bin/env python3
"""SEARCH button frame"""
import tkinter as tk
from ui.tk_helper import clear_colors
from ui.tk_helper import place
import ui.settings as s
from utils.models import DContent
from utils.models import DPage


class WikiPage(tk.Frame):
    def __init__(self, parent, entry):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        clear_colors()
        s.TARGET = entry.title()
        self.content = tk.Frame(parent, bg=s.FG, padx=10, pady=10)
        place(self.content, h=0.93, w=2, x=0.2, y=0.04, a="n")
        self.check_entry()

    def check_entry(self):
        q = DPage.select().where(DPage.name==s.TARGET)
        if len(q) != 0:
            self.draw_query(q[0], "cont obj")
        else:
            self.not_found()
            s.TARGET = ""

    def draw_query(self, page, cont):
        title = tk.Label(self.content, text=page.name)
        place(title, h=0.2, w=0.2, x=0.55, y=0.4)

    def not_found(self):
        self.error = tk.Frame(self.parent, bg=s.FG)
        self.error.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        message = tk.Label(self.error, text="Page not found.")
        place(message, h="", w=0.3, x=0.35, y=0.45)