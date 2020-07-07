#!/usr/bin/env python3
"""Update Page button frame"""
import tkinter as tk
from ui.tk_helper import place
import ui.settings as s
from ui.tk_helper import change_button_color
import ui.language as en
import utils.globals as g


class UpdatePage(tk.Frame):
    def __init__(self, parent, button):
        change_button_color(button)
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.target = None
        self.check_target()

    def check_target(self):
        if g.TARGET and g.TARGET != "":
            self.target = g.TARGET
            self.selection()
        else:
            self.no_selection()

    def selection(self):
        pass

    def no_selection(self):
        message_label = tk.Label(self.content, text=en.UP_ERR_1, bg=s.FG,
                                 fg=s.SEARCHFG, font=(s.FONT2, 14, "bold"))
        place(message_label, h=1, w=1, x=0, y=0)
