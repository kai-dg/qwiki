#!/usr/bin/env python3
"""Search by tags page"""
import tkinter as tk


class TagsPage(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=18)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")