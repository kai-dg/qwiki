#!/usr/bin/env python3
"""Add page button frame
entry -> check page info first -> check content -> format -> modelctrl ->
    form content -> make page -> print made page -> make content -> print made content
"""
import tkinter as tk
import ui.settings as s
from ui.tk_helper import place
from ui.tk_helper import change_button_color
import ui.language as en
from utils.models import Page
import utils.formatter as fm
from utils.models import set_ctrl
import utils.globals as g


def check_contents(data):
    """Data keys: page_name, header, contents"""
    if data["page_name"] == "":
        return False
    if data["header"] == "":
        return False
    return True

class AddPage(tk.Frame):
    def __init__(self, parent, button):
        """This page tracks display info, and actual data format for db.
        Vars:
            self.info: Changable text visual
            self.d_info: Display Information tracking
        """
        tk.Frame.__init__(self, parent)
        change_button_color(button)
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=18)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.page_data = g.PAGE_TEMPLATE
        self.d_info = []
        self.layout()
        self.labels()
        self.entries()
        self.buttons()
        self.display()

    def add_content(self, data):
        """Executing Add Content button."""
        self.errors["text"] = ""
        c = check_contents(data)
        if self.page_data["page_obj"] == None:
            q = Page.select().where(Page.name==data["page_name"])
            if len(q) != 0:
                self.errors["text"] = en.ERR_ADD1
        if c:
            self.content_text.delete("1.0", tk.END)
            self.title.delete(0, "end")
            self.page_data["page"]["name"] = data["page_name"]
            page = fm.format_title(data["page_name"])
            notes = fm.format_note(data["notes"])
            header = fm.format_header(data["header"])
            content = fm.format_content(data["content"])
            self.page_data["page"]["notes"] = notes
            self.page_data["cont"][g.IDX] = {
                "title": header,
                "cont": content
            }
            if g.IDX == 0:
                self.d_info.append(f"{page}{notes}")
                self.info["text"] = "".join(self.d_info)
            self.d_info.append(f"{header}{content}")
            self.info["text"] = "".join(self.d_info)
            g.IDX += 1
        else:
            print("adding erro")
            self.errors["text"] = en.ERR_ADD2

    def clear_all(self):
        """Clears all entry inputs on this page."""
        self.name.delete(0, "end")
        self.notes_entry.delete(0, "end")
        self.title.delete(0, "end")
        self.content_text.delete("1.0", tk.END)
        self.info["text"] = ""
        self.page_data["page"]["name"] = ""
        self.page_data["page"]["notes"] = ""
        self.page_data["cont"] = {}
        self.d_info = []
        g.IDX = 0

    def undo_one(self):
        """Deletes the current content index `s.IDX`, removes one item
        from end of `self.d_info`, -1 from `s.IDX`. Then refreshes text on 
        info display.
        """
        print(g.IDX, len(self.d_info))
        if g.IDX > 0:
            del self.page_data["cont"][g.IDX-1]
            popped = self.d_info.pop()
            g.IDX -= 1
        elif g.IDX == 0 and len(self.d_info) == 1:
            self.page_data["page"]["name"] = ""
            self.page_data["page"]["notes"] = ""
            popped = self.d_info.pop()
        self.info["text"] = "".join(self.d_info)


    def create_page(self):
        """Executing Create Page button."""
        Ctrl = set_ctrl()
        page = Ctrl.add_page(self.page_data["page"])
        self.page_data["page_obj"] = page["page"]
        cont = Ctrl.add_content(self.page_data["cont"], self.page_data["page_obj"])
        self.errors["text"] = page["message"]
        self.clear_all()

    def get_inputs(self) -> dict:
        """Gets all inputs from this page."""
        name = self.name.get()
        content = self.content_text.get("1.0", tk.END)
        header = self.title.get()
        notes = self.notes_entry.get()
        data = {
            "page_name": name.title(),
            "notes": notes.capitalize(),
            "header": header.capitalize(),
            "content": content
        }
        return data

    def display(self):
        self.info = tk.Label(self.right, bg=s.BG2, fg=s.SEARCHBG, wraplength=320,
                             anchor="nw", padx=20, pady=20, justify="left")
        place(self.info, h=0.92, w=1, x=0, y=0.08)
        self.errors = tk.Label(self.right, text="", anchor="w", bg=s.BG2,
                               fg=s.BUTTON_R, font=(s.FONT2, 12, "bold"), padx=10)
        place(self.errors, h=0.08, w=1, x=0, y=0)

    def labels(self):
        name_label = tk.Label(self.left, bg=s.FG, fg=s.TEXT1, text=en.LAB_ADD1,
                              font=(s.FONT1, 9))
        place(name_label, h="", w=0.2, x=0, y=0.0)
        notes_title = tk.Label(self.left, bg=s.FG, fg=s.TEXT1, text=en.LAB_ADD2,
                                 font=(s.FONT1, 9))
        place(notes_title, h="", w=0.2, x=0, y=0.05)
        content_title = tk.Label(self.left, bg=s.FG, fg=s.TEXT1, text=en.LAB_ADD3,
                                 font=(s.FONT1, 9))
        place(content_title, h="", w=0.2, x=0, y=0.14)

    def entries(self):
        self.name = tk.Entry(self.left, bg=s.SEARCHFG, fg=s.FG, font=(s.FONT2, 12))
        place(self.name, h="", w=0.67, x=0.25, y=0)
        self.notes_entry = tk.Entry(self.left, bg=s.SEARCHFG, fg=s.FG, font=(s.FONT2, 12))
        place(self.notes_entry, h="", w=0.67, x=0.25, y=0.05)
        self.title = tk.Entry(self.left, bg=s.SEARCHFG, fg=s.FG, font=(s.FONT2, 12))
        place(self.title, h="", w=0.67, x=0.25, y=0.14)
        self.content_text = tk.Text(self.left, bg=s.SEARCHBG, font=(s.FONT2, 9),
                                    fg=s.FG, padx=5, pady=5)
        place(self.content_text, h=0.35, w=0.98, x=0, y=0.20)

    def buttons(self):
        add = tk.Button(self.left, text=en.ADD_B1, font=(s.FONT1, 9),
                           bg=s.SEARCHBG, fg=s.TEXT3, command=lambda: self.add_content(self.get_inputs()))
        place(add, h="", w=0.3, x=0.33, y=0.575)
        undo = tk.Button(self.left, text=en.ADD_B2, font=(s.FONT1, 9),
                         bg=s.SEARCHBG, fg=s.TEXT3, command=lambda: self.undo_one())
        place(undo, h="", w=0.16, x=0.82, y=0.575)
        create = tk.Button(self.left, text=en.ADD_B3, font=(s.FONT1, 9),
                           bg=s.BUTTON_D, fg=s.TEXT1, command=lambda: self.create_page())
        place(create, h="", w=0.3, x=0.33, y=0.642)
        clear = tk.Button(self.left, text=en.ADD_B4, font=(s.FONT1, 9),
                          bg=s.SEARCHBG, fg=s.TEXT3, command=lambda: self.clear_all())
        place(clear, h="", w=0.16, x=0, y=0.575)

    def layout(self):
        """All partitions are relative to self.content"""
        self.left = tk.Frame(self.content, bg=s.FG)
        place(self.left, h=1, w=0.5, x=0, y=0)
        self.right = tk.Frame(self.content, bg=s.FG)
        place(self.right, h=1, w=0.5, x=0.5, y=0)
