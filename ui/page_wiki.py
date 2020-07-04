#!/usr/bin/env python3
"""SEARCH button frame"""
import tkinter as tk
import ui.settings as s


class WikiPage(tk.Frame):
    def __init__(self, parent, entry):
        tk.Frame.__init__(self, parent)
        s.TARGET = entry
        self.content = tk.Frame(parent, bg=s.FG)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        text = tk.Text(self.content, width=50, padx=10, pady=10, bg=s.FG, fg=s.SEARCHFG, font=(s.NORMAL_FONT, 11))
        text.place(relheight=1, relwidth=1, relx=0.5, rely=0, anchor="n")
        text.insert(tk.INSERT, entry)
