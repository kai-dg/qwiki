#!/usr/bin/env python3
"""Update Page button frame"""
import tkinter as tk
import ui.settings as s


class UpdatePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FOREGROUND)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        lab3 = tk.Label(self.content, bg="red", text=s.TARGET)
        lab3.pack()
