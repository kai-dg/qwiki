#!/usr/bin/env python3
import tkinter as tk
from ui.tk_helper import place
from ui.tk_helper import change_button_color
import ui.settings as s
import utils.formatter as fm
import ui.language as en
import utils.globals as g
from utils.models import set_query


class DelPage(tk.Frame):
    def __init__(self, parent, button):
        change_button_color(button)
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=18)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.target = None
        self.check_target()

    def check_target(self):
        if g.TARGET_PAGE and g.TARGET != "":
            self.target = g.TARGET
            self.selection()
        else:
            self.no_selection()

    def selection(self):
        frame = tk.Frame(self.content, bg=s.BG2)
        place(frame, h=0.4, w=0.9, x=0.05, y=0.2)
        title = tk.Label(frame, text=fm.format_title(g.TARGET).rstrip(),
                         font=(s.FONT1, 20, "bold"), bg=s.BG2, fg=s.SEARCHBG,
                         anchor="w", padx=25)
        notes = tk.Label(frame, text=g.TARGET_PAGE.notes.rstrip(),
                         font=(s.FONT1, 12, "bold"), bg=s.BG2, fg=s.SEARCHBG,
                         anchor="nw", padx=35)
        content = tk.Label(frame, text=g.TARGET_PAGE)
        place(title, h=0.2, w=1, x=0, y=0.03)
        place(notes, h=0.3, w=1, x=0, y=0.23)
        message = f"{en.CONFIRM_1} {self.target}?"
        self.message_label = tk.Label(self.content, text=message, bg=s.FG,
                                      fg=s.SEARCHBG, font=(s.FONT2, 12))
        place(self.message_label, h=0.1, w=1, x=0, y=0.6)
        self.buttons()

    def no_selection(self):
        message_label = tk.Label(self.content, text=en.CONFIRM_ERR_1, bg=s.FG,
                                 fg=s.SEARCHFG, font=(s.FONT2, 20, "bold"))
        place(message_label, h=1, w=1, x=0, y=0)

    def back(self):
        self.content.destroy()

    def delete_page(self):
        q = set_query(g.TARGET)
        q.page_obj = g.TARGET_PAGE
        cont = q.page_content()
        for c in cont:
            c.delete().execute()
        g.TARGET_PAGE.delete().execute()
        self.yes.destroy()
        self.no.destroy()
        self.message_label["text"] = f"{g.TARGET} {en.CONFIRM_SUCCESS}"
        
    def buttons(self):
        self.yes = tk.Button(self.content, text="Yes", bg=s.SEARCHBG, fg=s.TEXT3,
                             command=lambda: self.delete_page())
        place(self.yes, h="", w=0.15, x=0.3, y=0.7)
        self.no = tk.Button(self.content, text="No", bg=s.SEARCHBG, fg=s.TEXT3,
                            command=lambda: self.back())
        place(self.no, h="", w=0.15, x=0.55, y=0.7)