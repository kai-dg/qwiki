#!/usr/bin/env python3
import tkinter as tk
import ui.settings as s


def place(tk_obj, h, w, x, y, a=""):
    """Place order: relheight, relwidth, relx, rely.
    Wrapper for helping make the code more readable.
    Positions can be skipped with empty str.
    """
    if a != "":
        return tk_obj.place(relheight=h, relwidth=w, relx=x, rely=y, anchor=a)
    return tk_obj.place(relheight=h, relwidth=w, relx=x, rely=y)

def clear_colors():
	for i in s.MENU_BUTTONS.values():
		i.config(bg=s.SEARCHBG, fg=s.TEXT3)

def change_button_color(clicked):
	clear_colors()
	s.MENU_BUTTONS[clicked].config(bg=s.FG, fg=s.TEXT1)

if __name__ == "__main__":
    pass
