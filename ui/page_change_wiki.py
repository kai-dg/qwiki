#!/usr/bin/env python3
"""Add page button frame"""
import tkinter as tk
import ui.settings as s


class AddPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FOREGROUND)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        lab2 = tk.Label(self.content, text="helloadd")
        lab2.pack()
