#!/usr/bin/env python3
"""Add page button frame"""
import tkinter as tk
import ui.settings as s
from ui.tk_helper import place


def check_contents(data):
    """Data keys: page_name, header, contents"""
    if data["page_name"] == "":
        return False
    if data["header"] == "":
        return False
    return True

class AddPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=12)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.layout()
        self.labels()
        self.entries()
        self.buttons()
        self.text_and_display()

    def add_content(self, data):
        """Executing Add Content button."""
        self.errors["text"] = ""
        c = check_contents(data)
        if c:
            self.content_text.delete("1.0", tk.END)
            self.title.delete(0, "end")
            s.CONTENT[s.IDX] = {
                data["header"]: data["content"]
            }
            s.IDX += 1
            self.display["text"] += data["content"]
        else:
            self.errors["text"] = "ERROR: Page Name or Header is missing."

    def create_page(self):
        """Executing Create Page button. Resets global variables."""
        s.IDX = 0
        s.TARGET = 0
        s.CONTENT = {}
        s.PAGE_NAME = ""
        pass

    def get_inputs(self):
        name = self.name.get()
        content = self.content_text.get("1.0", tk.END)
        header = self.title.get()
        data = {
            "page_name": name,
            "header": header,
            "content": content
        }
        return data

    def text_and_display(self):
        self.content_text = tk.Text(self.middle, bg=s.SEARCHBG, font=(s.NORMAL_FONT, 9),
                                    fg=s.FG, padx=5, pady=5)
        place(self.content_text, h=0.7, w=1, x=0, y=0.1)
        self.display = tk.Label(self.right_side, text="", wraplength=100, anchor="nw",
                                justify="left", padx=10, pady=10, bg=s.BG2, fg=s.SEARCHBG)
        place(self.display, h=0.98, w=0.98, x=0.01, y=0.01)
        self.errors = tk.Label(self.middle, text="", anchor="c", bg=s.FG,
                               fg=s.TEXT1, font=(s.NORMAL_FONT, 12, "bold"))
        place(self.errors, h=0.05, w=1, x=0, y=0.885)

    def labels(self):
        name_label = tk.Label(self.top, bg=s.FG, fg=s.TEXT1, text="Page Name:",
                              font=(s.FONT1, 9))
        place(name_label, h="", w=0.2, x=0, y=0.15)
        content_title = tk.Label(self.middle, bg=s.FG, fg=s.TEXT1, text="Header:",
                                 font=(s.FONT1, 9))
        place(content_title, h="", w=0.2, x=0, y=0.03)

    def entries(self):
        self.title = tk.Entry(self.middle, bg=s.SEARCHFG, fg=s.FG, font=(s.NORMAL_FONT, 12))
        place(self.title, h="", w=0.68, x=0.25, y=0.03)
        self.name = tk.Entry(self.top, bg=s.SEARCHFG, fg=s.FG, font=(s.NORMAL_FONT, 12))
        place(self.name, h="", w=0.68, x=0.25, y=0.15)

    def buttons(self):
        add = tk.Button(self.middle, text="Add Content", font=(s.FONT1, 9),
                           bg=s.SEARCHBG, fg=s.TEXT3, command=lambda: self.add_content(self.get_inputs()))
        place(add, h="", w=0.3, x=0.33, y=0.82)
        create = tk.Button(self.bottom, text="Create Page", font=(s.FONT1, 9),
                           bg=s.SEARCHBG, fg=s.TEXT3)
        place(create, h="", w=0.3, x=0.33, y=0)

    def layout(self):
        """All partitions are relative to self.content"""
        self.top = tk.Frame(self.content, bg=s.FG)
        place(self.top, h=0.05, w=0.5, x=0, y=0)
        self.middle = tk.Frame(self.content, bg=s.FG)
        place(self.middle, h=0.92, w=0.5, x=0, y=0.05)
        self.bottom = tk.Frame(self.content, bg=s.FG)
        place(self.bottom, h=0.05, w=0.5, x=0, y=0.93)
        self.right_side = tk.Frame(self.content, bg=s.FG)
        place(self.right_side, h=1, w=0.5, x=0.5, y=0)
