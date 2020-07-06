#!/usr/bin/env python3
"""TODO, button info button for everything except get started"""
import tkinter as tk
import ui.language as en
from ui.tk_helper import place
from ui.tk_helper import change_button_color
import ui.settings as s


class HelpPage(tk.Frame):
    def __init__(self, parent, button):
        change_button_color(button)
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG, padx=10, pady=10)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        lab = tk.Label(self.content, text=en.WELCOME, font=(s.FONT1, 12, "bold"),
                       bg=s.FG, fg=s.SEARCHFG)
        lab.place(relheight=1, relwidth=1, relx=0, rely=0)
        triangle2 = tk.Canvas(self.content, bg=s.FG, highlightthickness=0)
        triangle2.create_polygon((0, 70, 35, 120, 70, 70), fill=s.BUTTON_R)
        start_here = tk.Label(self.content, bg=s.FG, fg=s.SEARCHFG, text=en.START_HELP,
                              font=(s.FONT1, 12, "bold"))
        place(triangle2, h=0.22, w=0.12, x=0.65, y=0.82)
        place(start_here, h=0.08, w=0.36, x=0.53, y=0.89)
        show_button = tk.Button(self.content, text=en.HELP_B1,
                                font=(s.FONT1, 9, "bold"), bg=s.SEARCHBG, fg=s.TEXT3,
                                command=lambda: self.show_more())
        place(show_button, h="", w=0.3, x=0.35, y=0.55)

    def show_more(self):
        tri1 = tk.Canvas(self.content, bg=s.FG, highlightthickness=0)
        tri1.create_polygon((0, 70, 35, 0, 70, 70), fill=s.SEARCHBG)
        name_help = tk.Label(self.content, bg=s.FG, fg=s.SEARCHFG, text=en.NAME_HELP,
                              font=(s.FONT1, 12, "bold"))
        place(tri1, h=0.22, w=0.12, x=0.04, y=0)
        place(name_help, h=0.07, w=0.18, x=0.5, y=0.05)

        tri3 = tk.Canvas(self.content, bg=s.FG, highlightthickness=0)
        tri3.create_polygon((0, 70, 35, 0, 70, 70), fill=s.SEARCHBG)
        searchbar = tk.Label(self.content, bg=s.FG, fg=s.SEARCHFG, text=en.SEARCH_HELP,
                              font=(s.FONT1, 12, "bold"))
        place(searchbar, h=0.07, w=0.2, x=0.4, y=0.05)
        place(tri3, h=0.22, w=0.12, x=0.45, y=0)

        tri4 = tk.Canvas(self.content, bg=s.FG, highlightthickness=0)
        tri4.create_polygon((0, 70, 35, 120, 70, 70), fill=s.SEARCHBG)
        place(tri4, h=0.22, w=0.12, x=0.05, y=0.82)
        # add page

        tri5 = tk.Canvas(self.content, bg=s.FG, highlightthickness=0)
        tri5.create_polygon((0, 70, 35, 120, 70, 70), fill=s.SEARCHBG)
        place(tri5, h=0.22, w=0.12, x=0.245, y=0.82)
        # update page

        tri5 = tk.Canvas(self.content, bg=s.FG, highlightthickness=0)
        tri5.create_polygon((0, 70, 35, 120, 70, 70), fill=s.SEARCHBG)
        place(tri5, h=0.22, w=0.12, x=0.45, y=0.82)
        # delete page