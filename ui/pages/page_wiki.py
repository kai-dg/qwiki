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
from ui.tk_styles import WikiPageStyles


class WikiPage(tk.Frame):
    def __init__(self, parent, entry):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        clear_colors()
        g.TARGET = entry.title().rstrip()
        self.content = tk.Frame(parent)
        place(self.content, h=0.93, w=2, x=0.2, y=0.04, a="n")
        self.base_f = tk.Frame(self.content)
        place(self.base_f, h=1, w=0.5, x=0.402, y=0)
        self.styles = WikiPageStyles(self)
        self.query_entry()

    def query_entry(self):
        """Implement fuzzy finder here. search -> query -> suggestions -> not_found"""
        q = g.QUERY.full_page_match(g.TARGET)
        if len(q) == 1 and g.TARGET != "":
            g.TARGET_PAGE = q[0]
            self.draw_query()
        if len(q) == 0:
            fuzz = g.QUERY.suggestions_match(g.TARGET)
            if len(fuzz) != 0:
                self.suggestions_page(fuzz)
            else:
                self.not_found()
                s.TARGET = ""

    def draw_query(self):
        cont = g.QUERY.page_content(g.TARGET_PAGE)
        g.TARGET_PAGE_CONT = cont
        cont_sects = {i: tk.Text for i in range(len(cont)*2)}
        row_amt = ((len(cont)*2) + 2)
        for r in range(row_amt):
            self.base_f.grid_rowconfigure(r, weight=0)
        self.base_f.grid_columnconfigure(0, weight=1)
        self.title_t = tk.Text(self.base_f)
        self.title_t.insert(tk.INSERT, g.TARGET_PAGE.name)
        self.title_t.config(state="disabled")
        self.title_t.grid(row=0, sticky="ewn", rowspan=1)
        self.notes_t = tk.Text(self.base_f)
        self.notes_t.insert(tk.INSERT, fm.format_note(g.TARGET_PAGE.notes).rstrip())
        new_height = int(round(float(self.notes_t.index(tk.END))))
        self.notes_t.config(height=new_height)
        self.notes_t.config(state="disabled")
        self.notes_t.grid(row=1, sticky="ewns", rowspan=1)
        row_idx = 2
        sect_idx = 0
        self.styles.draw_query(self)
        for c in cont:
            ctitle = cont_sects[sect_idx](self.base_f)    
            ctitle.insert(tk.INSERT, c.title)
            ctitle.config(state="disabled")
            ctitle.grid(row=row_idx, sticky="ewns", rowspan=1)
            self.styles.ctitle(ctitle)
            # bind click to changing font color
            content = cont_sects[sect_idx+1](self.base_f)
            content.insert(tk.INSERT, c.content.rstrip())
            new_height = int(round(float(content.index(tk.END))))
            content.config(height=new_height, state="disabled")
            content.grid(row=(row_idx+1), sticky="ewns", rowspan=1)
            self.styles.content(content)
            row_idx += 2
            sect_idx += 2

    def set_page(self, page_obj):
        """Refreshing base frame when clicking a suggestion item."""
        g.TARGET_PAGE = page_obj
        g.TARGET = page_obj.name
        self.base_f.destroy()
        self.base_f = tk.Frame(self.content)
        place(self.base_f, h=1, w=0.5, x=0.402, y=0)
        self.styles.set_page(self.base_f)
        
    def suggestions_page(self, q_list):
        sections = {}
        idx = 0
        col = 0
        ro = 0
        self.base_f.grid_columnconfigure(0, weight=1)
        for i in q_list:
            if idx == s.SUGGESTION_PG_LIMIT:
                ro = 0
                col = 1
                self.base_f.grid_columnconfigure(col, weight=1)
            self.base_f.grid_rowconfigure(ro, weight=1)
            self.base_f.grid_rowconfigure(ro+1, weight=1)
            qtitle_b = tk.Button(self.base_f, text=i.name, command=lambda m=i:
                                 [self.set_page(m), self.draw_query()])
            qtitle_b.grid(row=ro, column=col, sticky="w")
            self.styles.qtitle(qtitle_b)
            sections[idx] = qtitle_b
            notes = fm.format_note(i.notes)
            qnotes_l = tk.Label(self.base_f)
            qnotes_l.grid(row=(ro+1), column=col, sticky="nw")
            self.styles.qnotes(qnotes_l)
            sections[idx+1] = qnotes_l
            ro += 2
            idx += 2

    def not_found(self):
        self.err_f = tk.Frame(self.parent)
        place(self.err_f, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.message = tk.Label(self.err_f)
        place(self.message, h="", w=0.3, x=0.35, y=0.45)
