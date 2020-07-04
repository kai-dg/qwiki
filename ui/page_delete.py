#!/usr/bin/env python3
"""Delete Page button frame
TODO:
    delete page confirmation
    show page with delete button on bottom
"""
import tkinter as tk
import ui.settings as s


class DeletePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FOREGROUND)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
