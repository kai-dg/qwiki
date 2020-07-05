#!/usr/bin/env python3
"""Update Page button frame"""
import tkinter as tk
from ui.tk_helper import place
import ui.settings as s
from ui.tk_helper import change_button_color


class UpdatePage(tk.Frame):
    def __init__(self, parent, button):
        change_button_color(button)
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        lab3 = tk.Label(self.content, bg="red", text=s.TARGET)
        lab3.pack()
