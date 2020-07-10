#!/usr/bin/env python3
"""SEARCH button frame"""
import tkinter as tk
from ui.tk_helper import clear_colors
from ui.tk_helper import place
import ui.settings as s
from utils.models import set_query
import utils.formatter as fm
import ui.language as en
import utils.globals as g


class WikiPage(tk.Frame):
    def __init__(self, parent, entry):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        clear_colors()
        g.TARGET = entry.title().rstrip()
        self.content = tk.Frame(parent, bg=s.FG, padx=10, pady=10)
        place(self.content, h=0.93, w=2, x=0.2, y=0.04, a="n")
        self.base = tk.Frame(self.content, bg=s.FG, padx=25, pady=25)
        place(self.base, h=1, w=0.5, x=0.402, y=0)
        self.query_entry()

    def query_entry(self):
        """Implement fuzzy finder here. search -> query -> suggestions -> not_found"""
        q = g.QUERY.full_page_match(g.TARGET)
        if len(q) == 1:
            g.TARGET_PAGE = q[0]
            self.draw_query()
        else:
            q = g.QUERY.fuzzy_page_match(g.TARGET)
            self.suggestions_page(q)
        if len(q) == 0:
            self.not_found()
            s.TARGET = ""

    def draw_query(self):
        cont = g.QUERY.page_content(g.TARGET_PAGE)
        g.TARGET_PAGE_CONT = cont
        cont_sects = {i: tk.Text for i in range(len(cont)*2)}
        row_amt = ((len(cont)*2) + 2)
        for r in range(row_amt):
            self.base.grid_rowconfigure(r, weight=0)
        self.base.grid_columnconfigure(0, weight=1)
        title = tk.Text(self.base, relief="flat", wrap="word", bg=s.BG2, padx=15,
                        pady=10, fg=s.SEARCHBG, highlightthickness=0, height=1,
                        font=(s.FONT2, 25, "bold"))
        title.insert(tk.INSERT, g.TARGET_PAGE.name)
        title.config(state="disabled")
        title.grid(row=0, sticky="ewn", rowspan=1)
        notes = tk.Text(self.base, relief="flat", bg=s.BG2, padx=25,
                        pady=10, fg=s.SEARCHBG, highlightthickness=0, height=1,
                        font=(s.FONT2, 12, "italic"))
        notes.insert(tk.INSERT, fm.format_note(g.TARGET_PAGE.notes).rstrip())
        new_height = int(round(float(notes.index(tk.END))))
        notes.config(height=new_height)
        notes.config(state="disabled")
        notes.grid(row=1, sticky="ewns", rowspan=1)
        row_idx = 2
        sect_idx = 0
        for c in cont:
            ctitle = cont_sects[sect_idx](self.base, relief="flat", wrap="word", bg=s.BG2,
                             padx=15, pady=10, highlightthickness=0, height=1,
                             fg=s.SEARCHBG, font=(s.FONT2, 15, "bold"))    
            ctitle.insert(tk.INSERT, c.title)
            ctitle.config(state="disabled")
            ctitle.grid(row=row_idx, sticky="ewns", rowspan=1)
            # bind click to changing font color
            content = cont_sects[sect_idx+1](self.base, relief="flat", wrap="word", bg=s.BG2,
                              padx=24, pady=10,  highlightbackground=s.SEARCHBG,
                              fg=s.SEARCHBG, highlightthickness=1, height=5,
                              highlightcolor=s.SEARCHFG, font=(s.FONT2, 11))
            content.insert(tk.INSERT, c.content.rstrip())
            new_height = int(round(float(content.index(tk.END))))
            content.config(height=new_height)
            content.config(state="disabled")
            content.grid(row=(row_idx+1), sticky="ewns", rowspan=1)
            row_idx += 2
            sect_idx += 2

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

    def no_database(self):
        pass

    def not_found(self):
        self.error = tk.Frame(self.parent, bg=s.FG)
        self.error.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04,
                         anchor="n")
        message = tk.Label(self.error, text=en.WIKI_ERR1, font=(s.FONT2, 20,
                           "bold"), bg=s.FG, fg=s.SEARCHFG)
        place(message, h="", w=0.3, x=0.35, y=0.45)
