#!/usr/bin/env python3
"""Add page button frame
entry -> check page info first -> check content -> format -> modelctrl ->
    form content -> make page -> print made page -> make content -> print made content
"""
import tkinter as tk
import ui.settings as s
from ui.tk_helper import place
from ui.tk_helper import change_button_color
from utils.models import DPage
from utils.models import DContent
import utils.formatter as fm
from utils.models import set_ctrl


def check_contents(data):
    """Data keys: page_name, header, contents"""
    if data["page_name"] == "":
        return False
    if data["header"] == "":
        return False
    return True

class AddPage(tk.Frame):
    def __init__(self, parent, button):
        tk.Frame.__init__(self, parent)
        change_button_color(button)
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=18)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.page_data = s.PAGE_TEMPLATE
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
            q = DPage.select().where(DPage.name==data["page_name"])
            if len(q) != 0:
                self.errors["text"] = "ERROR: Page Name exists."
            else:
                self.page_data["page_obj"] = 0
        if c:
            self.content_text.delete("1.0", tk.END)
            self.title.delete(0, "end")
            self.page_data["page"]["name"] = data["page_name"] # For DB query
            page = fm.format_page(data["page_name"])
            notes = fm.format_note(data["notes"])
            header = fm.format_header(data["header"])
            content = fm.format_content(data["content"])
            self.page_data["page"]["notes"] = notes
            self.page_data["cont"][s.IDX] = {
                header: content
            }
            if s.IDX == 0:
                self.d_info.append(f"{page}{notes}")
                self.info["text"] = "".join(self.d_info)
            self.d_info.append(f"{header}{content}")
            self.info["text"] = "".join(self.d_info)
            s.IDX += 1
        else:
            self.errors["text"] = "ERROR: Page Name or Header is missing."

    def clear_all(self):
        self.name.delete(0, "end")
        self.notes_entry.delete(0, "end")
        self.info["text"] = ""
        self.page_data = s.PAGE_TEMPLATE
        self.d_info = []
        s.IDX = 0

    def undo_one(self):
        #TODO need to delete info page too
        if self.d_info != []:
            if s.IDX != 0:
                del self.d_info[s.IDX]
            else:
                popped = self.d_info.pop()
            self.info["text"] = "".join(self.d_info)
            s.IDX -= 1

    def create_page(self):
        """Executing Create Page button. Resets global variables."""
        Ctrl = set_ctrl()
        page = Ctrl.add_page(self.page_data["page"])
        self.errors["text"] = page["message"]
        self.clear_all()

    def get_inputs(self):
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
                               fg=s.TEXT1, font=(s.NORMAL_FONT, 12, "bold"), padx=10)
        place(self.errors, h=0.08, w=1, x=0, y=0)

    def labels(self):
        name_label = tk.Label(self.left, bg=s.FG, fg=s.TEXT1, text="Page Name:",
                              font=(s.FONT1, 9))
        place(name_label, h="", w=0.2, x=0, y=0.0)
        notes_title = tk.Label(self.left, bg=s.FG, fg=s.TEXT1, text="Notes:",
                                 font=(s.FONT1, 9))
        place(notes_title, h="", w=0.2, x=0, y=0.05)
        content_title = tk.Label(self.left, bg=s.FG, fg=s.TEXT1, text="Header:",
                                 font=(s.FONT1, 9))
        place(content_title, h="", w=0.2, x=0, y=0.14)

    def entries(self):
        self.name = tk.Entry(self.left, bg=s.SEARCHFG, fg=s.FG, font=(s.NORMAL_FONT, 12))
        place(self.name, h="", w=0.67, x=0.25, y=0)
        self.notes_entry = tk.Entry(self.left, bg=s.SEARCHFG, fg=s.FG, font=(s.NORMAL_FONT, 12))
        place(self.notes_entry, h="", w=0.67, x=0.25, y=0.05)
        self.title = tk.Entry(self.left, bg=s.SEARCHFG, fg=s.FG, font=(s.NORMAL_FONT, 12))
        place(self.title, h="", w=0.67, x=0.25, y=0.14)
        self.content_text = tk.Text(self.left, bg=s.SEARCHBG, font=(s.NORMAL_FONT, 9),
                                    fg=s.FG, padx=5, pady=5)
        place(self.content_text, h=0.65, w=0.98, x=0, y=0.20)

    def buttons(self):
        add = tk.Button(self.left, text="Add Content", font=(s.FONT1, 9),
                           bg=s.SEARCHBG, fg=s.TEXT3, command=lambda: self.add_content(self.get_inputs()))
        place(add, h="", w=0.3, x=0.33, y=0.875)
        undo = tk.Button(self.left, text="Undo", font=(s.FONT1, 9),
                         bg=s.SEARCHBG, fg=s.TEXT3, command=lambda: self.undo_one())
        place(undo, h="", w=0.16, x=0.82, y=0.875)
        create = tk.Button(self.left, text="Create Page", font=(s.FONT1, 9),
                           bg=s.BUTTON_D, fg=s.TEXT1, command=lambda: self.create_page())
        place(create, h="", w=0.3, x=0.33, y=0.942)
        clear = tk.Button(self.left, text="Clear", font=(s.FONT1, 9),
                          bg=s.SEARCHBG, fg=s.TEXT3, command=lambda: self.clear_all())
        place(clear, h="", w=0.16, x=0, y=0.875)

    def layout(self):
        """All partitions are relative to self.content"""
        self.left = tk.Frame(self.content, bg=s.FG)
        place(self.left, h=1, w=0.5, x=0, y=0)
        self.right = tk.Frame(self.content, bg=s.FG)
        place(self.right, h=1, w=0.5, x=0.5, y=0)
