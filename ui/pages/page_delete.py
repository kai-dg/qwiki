#!/usr/bin/env python3
import tkinter as tk
from ui.tk_helper import place
from ui.tk_helper import change_button_color
import ui.settings as s
import utils.formatter as fm
import ui.language as en
import utils.globals as g
from ui.tk_styles import DelPageStyles


class DelPage(tk.Frame):
    def __init__(self, parent, button):
        change_button_color(button)
        tk.Frame.__init__(self, parent)
        self.base_f = tk.Frame(None)
        place(self.base_f, h=0.93, w=1, x=0, y=0.04)
        self.target = None
        self.styles = DelPageStyles(self)
        self.check_target()

    def check_target(self):
        if g.TARGET_PAGE and g.TARGET != "":
            self.target = g.TARGET
            self.selection()
        else:
            self.no_selection()

    def selection(self):
        self.title_l = tk.Label(self.base_f, text=fm.format_title(
                                g.TARGET).rstrip())
        self.notes_l = tk.Label(self.base_f, text=g.TARGET_PAGE.notes.rstrip())
        place(self.title_l, h=0.2, w=1, x=0, y=0.03)
        place(self.notes_l, h=0.3, w=1, x=0, y=0.23)
        message = f"{en.CONFIRM_1} {self.target}?"
        self.message_l = tk.Label(self.base_f, text=message)
        place(self.message_l, h=0.1, w=1, x=0, y=0.6)
        self.styles.selection(self)
        self.buttons()

    def no_selection(self):
        self.err_l = tk.Label(self.base_f)
        place(self.err_l, h=1, w=1, x=0, y=0)
        self.styles.no_selection(self)

    def back(self):
        self.base_f.destroy()

    def delete_page(self):
        g.MODELCTRL.delete_content(g.TARGET_PAGE)
        g.MODELCTRL.delete_page(g.TARGET)
        self.message_l["text"] = f"{g.TARGET} {en.CONFIRM_SUCCESS}"
        g.TARGET_PAGE_CONT = None
        g.TARGET_PAGE = None
        g.TARGET = ""
        self.yes_b.destroy()
        self.no_b.destroy()
        
    def buttons(self):
        self.yes_b = tk.Button(self.base_f, command=lambda: self.delete_page())
        place(self.yes_b, h="", w=0.15, x=0.3, y=0.7)
        self.no_b = tk.Button(self.base_f, command=lambda: self.back())
        place(self.no_b, h="", w=0.15, x=0.55, y=0.7)
        self.styles.buttons(self)