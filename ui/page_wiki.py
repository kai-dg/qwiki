#!/usr/bin/env python3
"""SEARCH button frame"""
import tkinter as tk
from ui.tk_helper import clear_colors
from ui.tk_helper import place
import ui.settings as s
from utils.models import set_query
import utils.formatter as fm
import ui.language as en


class WikiPage(tk.Frame):
    def __init__(self, parent, entry):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        clear_colors()
        s.TARGET = entry.title()
        self.content = tk.Frame(parent, bg=s.FG, padx=10, pady=10)
        place(self.content, h=0.93, w=2, x=0.2, y=0.04, a="n")
        self.Query = set_query(s.TARGET)
        self.base = tk.Frame(self.content, bg=s.BG2, padx=25, pady=25)
        self.query_entry()

    def draw_query(self, page):
        cont = page.content
        sections = {i: tk.Label for i in range(len(cont)*2)}
        ptitle = fm.format_title(page.name)
        all_page = f"{ptitle}{page.notes}"
        title = tk.Label(self.base, text=ptitle.rstrip(), font=(s.FONT1, 22, "bold"),
                         bg=s.BG2, fg=s.SEARCHBG, justify="left")
        title.grid(row=1, sticky="w", rowspan=1)
        notes = tk.Label(self.base, text=page.notes, font=(s.FONT1, 12), bg=s.BG2,
                         fg=s.SEARCHBG, justify="left")
        notes.grid(row=2, sticky="w", rowspan=1, padx=10)
        idx = 0
        for c in cont:
            temp = f"{c.title}{c.content}"
            ctitle = sections[idx](self.base, text=c.title.rstrip(), justify="left", bg=s.BG2,
                                   fg=s.SEARCHBG, font=(s.FONT1, 17, "bold"))
            ctitle.grid(row=(idx+3), columnspan=1, sticky="w")
            ccontent = sections[idx+1](self.base, text=c.content, justify="left", bg=s.BG2,
                                       fg=s.SEARCHBG, font=(s.FONT1, 12))
            ccontent.grid(row=(idx+4), columnspan=1, sticky="w")
            idx += 2

    def suggestions_page(self, q_list):
        sections = {i: tk.Label for i in range(len(q_list)*2)}
        idx = 0
        for i in q_list:
            qtitle = sections[idx](self.base, text=i.name.rstrip(), justify="left")
            qtitle.grid(row=(idx+1), columnspan=1, sticky="w")
            qnotes = sections[idx](self.base, text=i.notes.rstrip(), justify="left",
                                    padx=12)
            qnotes.grid(row=(idx+2), columnspan=1, sticky="w")
            idx += 2

    def query_entry(self):
        """Implement fuzzy finder here. search -> query -> suggestions -> not_found"""
        q = self.Query.full_page_match()
        place(self.base, h=1, w=0.5, x=0.402, y=0)
        if len(q) == 1:
            self.draw_query(q[0])
        else:
            q = self.Query.fuzzy_page_match()
            self.suggestions_page(q)
        if len(q) == 0:
            self.not_found()
            s.TARGET = ""

    def not_found(self):
        self.error = tk.Frame(self.parent, bg=s.FG)
        self.error.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        message = tk.Label(self.error, text=en.WIKI_ERR1)
        place(message, h="", w=0.3, x=0.35, y=0.45)
