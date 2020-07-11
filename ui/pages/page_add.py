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
import utils.formatter as fm
import utils.globals as g
from copy import deepcopy


def check_contents(data):
    """Data keys: page_name, header, contents"""
    res = {"ok": True}
    if data["page_name"] == "":
        res["ok"] = False
    if data["header"] == "":
        res["ok"] = False
    q = g.QUERY.pages(data["page_name"])
    if len(q) != 0:
        res["ok"] = False
    return res

class AddPage(tk.Frame):
    def __init__(self, parent, button):
        tk.Frame.__init__(self, parent)
        change_button_color(button)
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=18)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.page_data = deepcopy(g.PAGE_TEMPLATE)
        self.err_amt = 3
        self.errors = {i: tk.Text for i in range(self.err_amt)}
        self.display_objs = []
        self.layout()
        self.labels()
        self.entries()
        self.buttons()
        self.display()

    def reset_errors(self):
        for v in self.errors.values():
            #v.config(state="normal")
            v.delete("1.0", tk.END)
            #v.config(state="disabled")

    def get_inputs(self) -> dict:
        """Gets all inputs from this page."""
        name = self.name.get()
        content = self.content_text.get("1.0", tk.END)
        header = self.title.get().title()
        notes = self.notes_entry.get()
        data = {
            "page_name": name.rstrip().title(),
            "notes": fm.format_note(notes),
            "header": header.rstrip().title(),
            "content": fm.format_content(content)
        }
        return data

    def add_content(self, data):
        """Executing Add Content button.
        """
        self.reset_errors()
        check = check_contents(data)
        pages = g.QUERY.pages(data["page_name"])
        if check["ok"] and len(pages) == 0:
            # reset Entry for content title and content
            self.content_text.delete("1.0", tk.END)
            self.title.delete(0, "end")
            # set page
            self.page_data["page"]["name"] = data["page_name"]
            self.page_data["page"]["notes"] = data["notes"]
            # set content with idx
            self.page_data["cont"][g.IDX] = {
                "title": data["header"],
                "cont": data["content"]
            }
            g.IDX += 1
            self.grid_data()
        else:
            if len(pages) != 0:
                self.errors[0].config(state="normal")
                self.errors[0].insert(tk.INSERT, en.ERR_ADD1)
                self.errors[1].config(state="disabled")
            self.errors[1].config(state="normal")
            self.errors[1].insert(tk.INSERT, en.ERR_ADD2)
            self.errors[1].config(state="disabled")

    def grid_data(self):
        page = self.page_data["page"]
        page_row = tk.Text(self.info, bg=s.FG, font=(s.FONT2, 17, "bold"),
                           wrap="word", relief="flat", height=1, fg=s.SEARCHFG)
        page_row.insert(tk.INSERT, page["name"])
        page_row.grid(row=self.err_amt, sticky="ewns", rowspan=1)
        notes_row = tk.Text(self.info, bg=s.FG, font=(s.FONT2, 9, "italic"),
                           wrap="word", relief="flat", height=1, fg=s.SEARCHFG)
        notes_row.insert(tk.INSERT, page["notes"])
        new_height = int(round(float(notes_row.index(tk.END))))
        notes_row.config(height=new_height)
        notes_row.grid(row=self.err_amt+1, sticky="ewns", rowspan=1)
        self.display_objs.append([page_row, notes_row])
        cont = self.page_data["cont"]
        row_idx = self.err_amt + 2
        for idx, v in cont.items():
            self.info.grid_rowconfigure(row_idx, weight=0)
            self.info.grid_rowconfigure(row_idx+1, weight=0)
            title = tk.Text(self.info, bg=s.FG, font=(s.FONT2, 12, "bold"),
                            wrap="word", relief="flat", height=1, fg=s.SEARCHBG)
            title.insert(tk.INSERT, v["title"])
            title.config(state="disabled")
            title.grid(row=(row_idx), sticky="ewns", rowspan=1)
            content = tk.Text(self.info, bg=s.FG, font=(s.FONT2, 8),
                            wrap="word", relief="flat", height=1, fg=s.SEARCHFG)
            content.insert(tk.INSERT, v["cont"])
            content.config(state="disabled")
            new_height = int(round(float(content.index(tk.END))))
            content.config(height=new_height)
            content.grid(row=(row_idx+1), sticky="ewns", rowspan=1)
            self.display_objs.append([title, content])
            row_idx += 2

    def clear_all(self):
        """Clears all entry inputs on this page."""
        for o in self.display_objs:
            o[0].destroy()
            o[1].destroy()
        self.reset_errors()
        self.name.delete(0, "end")
        self.notes_entry.delete(0, "end")
        self.title.delete(0, "end")
        self.page_data = deepcopy(g.PAGE_TEMPLATE)
        g.IDX = 0

    def undo_one(self):
        """Undos previous Add Content"""
        if self.display_objs != []:
            for o in self.display_objs[-1]:
                o.destroy()
            popped = self.display_objs.pop()
        if len(self.display_objs) > 1:
            del self.page_data["cont"][g.IDX-1]
        else:
            self.page_data = deepcopy(g.PAGE_TEMPLATE)

    def create_page(self):
        """Executing Create Page button."""
        if self.page_data["page"]["name"] != "":
            page = g.MODELCTRL.add_page(self.page_data["page"])
            g.MODELCTRL.add_content(self.page_data["cont"], page)
            self.clear_all()
            self.errors[0].config(state="normal")
            self.errors[0].insert(tk.INSERT, f"{en.ADD_OK1} {page.name}")
            self.errors[1].config(state="disabled")
        else:
            self.errors[0].config(state="normal")
            self.errors[0].insert(tk.INSERT, en.ERR_ADD2)
            self.errors[1].config(state="disabled")


    def display(self):
        self.info = tk.Frame(self.right, bg=s.FG, padx=20, pady=20)
        place(self.info, h=1, w=1, x=0, y=0)
        self.info.grid_columnconfigure(0, weight=1)
        for e in range(0, len(self.errors.keys())):
            self.info.grid_rowconfigure(e, weight=0)
            err = self.errors[e](self.info, bg=s.FG, font=(s.FONT2, 10, "bold"),
                                 wrap="word", relief="flat", height=1,
                                 fg=s.BUTTON_R)
            err.config(state="disabled")
            err.grid(row=e, sticky="ewns", rowspan=1)
            self.errors[e] = err
        self.info.grid_rowconfigure(self.err_amt, weight=0) # page title row
        self.info.grid_rowconfigure(self.err_amt+1, weight=0) # page notes row

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
