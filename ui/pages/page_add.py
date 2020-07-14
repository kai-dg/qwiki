#!/usr/bin/env python3
"""Add page button frame
entry -> check page info first -> check content -> format -> modelctrl ->
    form content -> make page -> print made page -> make content -> print made content
"""
import tkinter as tk
import ui.settings as s
from ui.tk_helper import place
from ui.tk_helper import change_button_color
from ui.tk_styles import AddPageStyles
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
        self.base_f = tk.Frame(None)
        place(self.base_f, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.page_data = deepcopy(g.PAGE_TEMPLATE)
        self.err_amt = 3
        self.errors = {i: tk.Text for i in range(self.err_amt)}
        self.display_objs = []
        self.layout()
        self.labels()
        self.entries()
        self.buttons()
        self.styles = AddPageStyles(self)
        self.display()

    def reset_errors(self):
        for v in self.errors.values():
            #v.config(state="normal")
            v.delete("1.0", tk.END)
            #v.config(state="disabled")

    def get_inputs(self) -> dict:
        """Gets all inputs from this page."""
        name = self.name_e.get()
        content = self.content_t.get("1.0", tk.END)
        header = self.title_e.get().title()
        notes = self.notes_e.get()
        data = {
            "page_name": name.rstrip().title(),
            "notes": notes,
            "header": header.rstrip().title(),
            "content": content
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
            self.content_t.delete("1.0", tk.END)
            self.title_e.delete(0, "end")
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
        page_row = tk.Text(self.display_f)
        self.styles.page_title(page_row)
        page_row.insert(tk.INSERT, page["name"])
        page_row.grid(row=self.err_amt, sticky="ewns", rowspan=1)
        notes_row = tk.Text(self.display_f)
        self.styles.page_notes(notes_row)
        notes_row.insert(tk.INSERT, page["notes"])
        new_height = int(round(float(notes_row.index(tk.END))))
        notes_row.config(height=new_height)
        notes_row.grid(row=self.err_amt+1, sticky="ewns", rowspan=1)
        self.display_objs.append([page_row, notes_row])
        cont = self.page_data["cont"]
        row_idx = self.err_amt + 2
        for idx, v in cont.items():
            self.display_f.grid_rowconfigure(row_idx, weight=0)
            self.display_f.grid_rowconfigure(row_idx+1, weight=0)
            title = tk.Text(self.display_f)
            self.styles.content_title(title)
            title.insert(tk.INSERT, v["title"])
            title.config(state="disabled")
            title.grid(row=(row_idx), sticky="ewns", rowspan=1)
            content = tk.Text(self.display_f)
            self.styles.content(content)
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
        self.name_e.delete(0, "end")
        self.notes_e.delete(0, "end")
        self.title_e.delete(0, "end")
        self.page_data = deepcopy(g.PAGE_TEMPLATE)
        g.IDX = 0

    def undo_one(self):
        """Undos previous Add Content"""
        print("before ", self.display_objs)
        if self.display_objs != []:
            for o in self.display_objs[-1]:
                o.destroy()
            popped = self.display_objs.pop()
        if len(self.display_objs) > 1:
            del self.page_data["cont"][g.IDX-1]
        else:
            self.page_data = deepcopy(g.PAGE_TEMPLATE)
        print("after ", self.display_objs)

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
        self.display_f = tk.Frame(self.right)
        place(self.display_f, h=1, w=1, x=0, y=0)
        self.display_f.grid_columnconfigure(0, weight=1)
        self.styles.display(self)
        for e in range(0, len(self.errors.keys())):
            self.display_f.grid_rowconfigure(e, weight=0)
            err = self.errors[e](self.display_f)
            self.styles.errors(err)
            err.config(state="disabled")
            err.grid(row=e, sticky="ewns", rowspan=1)
            self.errors[e] = err
        self.display_f.grid_rowconfigure(self.err_amt, weight=0) # page title row
        self.display_f.grid_rowconfigure(self.err_amt+1, weight=0) # page notes row

    def labels(self):
        self.name_l = tk.Label(self.layout_left_f)
        place(self.name_l, h="", w=0.2, x=0, y=0.0)
        self.notes_l = tk.Label(self.layout_left_f)
        place(self.notes_l, h="", w=0.2, x=0, y=0.05)
        self.c_title_l = tk.Label(self.layout_left_f)
        place(self.c_title_l, h="", w=0.2, x=0, y=0.14)

    def entries(self):
        self.name_e = tk.Entry(self.layout_left_f)
        place(self.name_e, h="", w=0.67, x=0.25, y=0)
        self.notes_e = tk.Entry(self.layout_left_f)
        place(self.notes_e, h="", w=0.67, x=0.25, y=0.05)
        self.title_e = tk.Entry(self.layout_left_f)
        place(self.title_e, h="", w=0.67, x=0.25, y=0.14)
        self.content_t = tk.Text(self.layout_left_f)
        place(self.content_t, h=0.35, w=0.98, x=0, y=0.20)

    def buttons(self):
        self.add_b = tk.Button(self.layout_left_f, command=lambda:
                               self.add_content(self.get_inputs()))
        place(self.add_b, h="", w=0.3, x=0.33, y=0.575)
        self.undo_b = tk.Button(self.layout_left_f, command=lambda:
                                self.undo_one())
        place(self.undo_b, h="", w=0.16, x=0.82, y=0.575)
        self.create_b = tk.Button(self.layout_left_f, command=lambda:
                                  self.create_page())
        place(self.create_b, h="", w=0.3, x=0.33, y=0.642)
        self.clear_b = tk.Button(self.layout_left_f, command=lambda:
                                 self.clear_all())
        place(self.clear_b, h="", w=0.16, x=0, y=0.575)

    def layout(self):
        """All partitions are relative to self.content"""
        self.layout_left_f = tk.Frame(self.base_f)
        place(self.layout_left_f, h=1, w=0.5, x=0, y=0)
        self.right = tk.Frame(self.base_f, bg=s.FG)
        place(self.right, h=1, w=0.5, x=0.5, y=0)
