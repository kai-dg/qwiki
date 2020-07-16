#!/usr/bin/env python3
"""SEARCH button frame"""
import tkinter as tk
import ui.tk_helper as tkh
import ui.settings as s
from utils.models import set_query
import utils.formatter as fm
import ui.language as en
import utils.globals as g
from ui.tk_styles import WikiPageStyles
from tkinter import ttk


class WikiPage(tk.Frame):
    def __init__(self, parent, button=None):
        tk.Frame.__init__(self, parent)
        tkh.clear_colors()
        self.canvas = tk.Canvas(None)
        self.base_f = tk.Frame(self.canvas)
        self.draw_scrollbar()
        self.styles = WikiPageStyles(self)
        tkh.place(self.canvas, h=0.93, w=1, x=0, y=0.04)
        self.query_entry()

    def draw_scrollbar(self):
        self.base_f.bind("<Configure>", lambda e: self.canvas.configure(
                         scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.base_f, anchor="nw")
        self.scroll = tk.Scrollbar(self.canvas, orient="vertical",
                                   command=self.canvas.yview)
        self.scroll.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.
                             yview_scroll(int(-2*(event.delta/120)), "units"))

    def query_entry(self):
        """Matches query with exact match, then a fuzzy search"""
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
        """Creates the query's wiki page"""
        tkh.display_page(self)
        self.styles.display_page(self)
        self.styles.disable_text(self)

    def set_page(self, page_obj):
        """Refreshing base frame when clicking a suggestion item."""
        g.TARGET_PAGE = page_obj
        g.TARGET = page_obj.name
        self.base_f.destroy()
        self.base_f = tk.Frame(self.canvas)
        self.scroll.destroy()
        self.draw_scrollbar()
        self.styles.set_page(self)
        
    def suggestions_page(self, q_list):
        sections = {}
        idx = 0
        col = 0
        ro = 0
        self.base_f.grid_columnconfigure(0, weight=1)
        for i in q_list:
            self.base_f.grid_rowconfigure(ro, weight=0)
            self.base_f.grid_rowconfigure(ro+1, weight=0)
            qtitle_b = tk.Button(self.base_f, text=i.name, command=lambda m=i:
                                 [self.set_page(m), self.draw_query()])
            qtitle_b.grid(row=ro, sticky="we", rowspan=1)
            self.styles.qtitle(qtitle_b)
            sections[idx] = qtitle_b
            notes = fm.format_note(i.notes)
            qnotes_l = tk.Label(self.base_f, text=notes)
            qnotes_l.grid(row=(ro+1), sticky="nwe", rowspan=1)
            self.styles.qnotes(qnotes_l)
            sections[idx+1] = qnotes_l
            ro += 2
            idx += 2

    def not_found(self):
        self.err_f = tk.Frame(self.base_f)
        tkh.place(self.err_f, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.message = tk.Label(self.err_f)
        tkh.place(self.message, h="", w=0.3, x=0.35, y=0.45)
