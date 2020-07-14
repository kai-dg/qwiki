#!/usr/bin/env python3
"""Tkinter related functions"""
import tkinter as tk
import ui.settings as s
import utils.globals as g
import utils.formatter as fm


def place(tk_obj, h, w, x, y, a=""):
    """Place order: relheight, relwidth, relx, rely.
    Wrapper for helping make the code more readable.
    Positions can be skipped with empty str.
    """
    if a != "":
        return tk_obj.place(relheight=h, relwidth=w, relx=x, rely=y, anchor=a)
    return tk_obj.place(relheight=h, relwidth=w, relx=x, rely=y)

def clear_colors():
	for i in g.MENU_BUTTONS.values():
		i.config(bg=s.SEARCHBG, fg=s.TEXT3)

def change_button_color(clicked):
	clear_colors()
	g.MENU_BUTTONS[clicked].config(bg=s.FG, fg=s.TEXT1)

def refresh_globals():
    """Refreshes globals that don't need to be carried anymore"""
    g.TARGET_PAGE = None
    g.TARGET = ""

def create_cont_sects():
    data = {}
    page_idx = 0
    for i in g.TARGET_PAGE_CONT:
        data[page_idx] = {"tk": tk.Text, "idx": i.idx, "title": i.title}
        data[page_idx+1] = {"tk": tk.Text, "idx": i.idx, "content": i.content}
        page_idx += 2
    return data

def display_page(pg):
    """Takes in the self of a page to draw a query page"""
    side_pad = 20
    cont = g.QUERY.page_content(g.TARGET_PAGE)
    g.TARGET_PAGE_CONT = cont
    pg.cont_sects = create_cont_sects()
    #pg.cont_sects = {i: tk.Text for i in range(len(cont)*2)}
    row_amt = ((len(cont)*2) + 2)
    for r in range(row_amt):
        pg.base_f.grid_rowconfigure(r, weight=0)
    pg.base_f.grid_columnconfigure(0, weight=0)
    pg.title_t = tk.Text(pg.base_f)
    pg.title_t.insert(tk.INSERT, g.TARGET_PAGE.name)
    pg.title_t.grid(row=0, sticky="ewn", rowspan=1, ipadx=side_pad)
    pg.notes_t = tk.Text(pg.base_f)
    pg.notes_t.insert(tk.INSERT, fm.format_note(g.TARGET_PAGE.notes).rstrip())
    new_height = int(round(float(pg.notes_t.index(tk.END))))
    pg.notes_t.config(height=new_height)
    pg.notes_t.grid(row=1, sticky="ewns", rowspan=1, ipadx=side_pad)
    row_idx = 2
    sect_idx = 0
    for c in cont:
        ctitle = pg.cont_sects[sect_idx]["tk"](pg.base_f)
        ctitle.insert(tk.INSERT, c.title)
        ctitle.grid(row=row_idx, sticky="ewns", rowspan=1, ipadx=side_pad)
        pg.cont_sects[sect_idx]["tk"] = ctitle
        # TODO bind click to changing font color
        content = pg.cont_sects[sect_idx+1]["tk"](pg.base_f)
        content.insert(tk.INSERT, c.content.rstrip())
        new_height = int(round(float(content.index(tk.END))))
        content.grid(row=(row_idx+1), sticky="ewns", rowspan=1, ipadx=side_pad)
        content.config(height=new_height)
        pg.cont_sects[sect_idx+1]["tk"] = content
        row_idx += 2
        sect_idx += 2