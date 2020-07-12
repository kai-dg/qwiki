#!/usr/bin/env python3
"""Update Page button frame"""
import tkinter as tk
from ui.tk_helper import place
import ui.settings as s
from ui.tk_helper import change_button_color
from ui.tk_helper import clear_colors
from ui.tk_styles import UpdatePageStyles
import ui.language as en
import utils.globals as g
from utils.models import set_ctrl


class UpdatePage(tk.Frame):
    def __init__(self, parent, button):
        change_button_color(button)
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.styles = UpdatePageStyles(self)
        self.check_target()

    def check_target(self):
        if g.TARGET_PAGE and g.TARGET != "":
            self.selection()
        else:
            self.no_selection()

    def selection(self):
        self.base_f = tk.Frame(self.content)
        self.styles.selection(self)
        place(self.base_f, h=1, w=1, x=0, y=0)
        self.draw_selection()

    def no_selection(self):
        self.message_l = tk.Label(self.content)
        place(self.message_l, h=1, w=1, x=0, y=0)
        self.styles.no_selection(self)

    def create_cont_sects(self):
        data = {}
        page_idx = 0
        for i in g.TARGET_PAGE_CONT:
            data[page_idx] = {"tk": tk.Text, "idx": i.idx, "title": i.title}
            data[page_idx+1] = {"tk": tk.Text, "idx": i.idx, "content": i.content}
            page_idx += 2
        return data

    def draw_selection(self):
        self.cont_sects = self.create_cont_sects()
        row_amt = ((len(list(self.cont_sects))) + 3)
        self.buttons(row_amt)
        for r in range(row_amt):
            self.base_f.grid_rowconfigure(r, weight=0)
        self.base_f.grid_columnconfigure(0, weight=1)
        self.title_t = tk.Text(self.base_f)
        self.title_t.insert(tk.INSERT, g.TARGET_PAGE.name)
        self.title_t.grid(row=0, sticky="ewn", rowspan=1)
        self.notes_t = tk.Text(self.base_f)
        self.notes_t.insert(tk.INSERT, g.TARGET_PAGE.notes)
        new_height = int(round(float(self.notes_t.index(tk.END))))
        self.notes_t.config(height=new_height)
        self.notes_t.grid(row=1, sticky="ewns", rowspan=1)
        self.styles.draw_selection(self)
        for idx, data in self.cont_sects.items():
            if data.get("title", "") != "":
                ctitle = data["tk"](self.base_f)
                self.styles.c_title(ctitle)
                ctitle.insert(tk.INSERT, data["title"])
                ctitle.grid(row=idx+2, sticky="ewns", rowspan=1)
                data["tk"] = ctitle
            else:
            # bind click to changing font color
                content = data["tk"](self.base_f)
                self.styles.content(content)
                content.insert(tk.INSERT, data["content"])
                new_height = int(round(float(content.index(tk.END))))
                content.config(height=new_height)
                content.grid(row=idx+2, sticky="ewns", rowspan=1)
                data["tk"] = content


    def buttons(self, row_idx):
        self.button_f = tk.Frame(self.base_f)
        self.button_f.grid(row=row_idx, sticky="ewns", rowspan=1)
        self.button_f.grid_columnconfigure(0, weight=1)
        self.button_f.grid_columnconfigure(1, weight=1)
        self.save_b = tk.Button(self.button_f, command=lambda: self.save())
        self.save_b.grid(row=0, column=0, sticky="ewns", padx=10, pady=20)
        self.cancel_b = tk.Button(self.button_f, command=lambda: self.cancel())
        self.cancel_b.grid(row=0, column=1, sticky="ewns", padx=10, pady=20)
        self.styles.buttons(self)

    def save(self):
        """Updates self.cont_sects, self.title, and self.notes.
        Formats self.cont_sects into data for updating Content model.
        """
        data = {
            "name": self.title_t.get("1.0", tk.END),
            "notes": self.notes_t.get("1.0", tk.END)
        }
        if data["name"] != g.TARGET_PAGE.name:
            self.title_t.update()
            data["name"] = self.title_t.get("1.0", tk.END).rstrip().title()
            new_page = g.MODELCTRL.update_page(g.TARGET, data)
        if data["notes"] != g.TARGET_PAGE.notes:
            self.notes_t.update()
            data["notes"] = self.notes_t.get("1.0", tk.END).rstrip()
            new_page = g.MODELCTRL.update_page(g.TARGET, data)
        g.TARGET = self.title_t.get("1.0", tk.END).rstrip().title()
        g.TARGET_PAGE = g.QUERY.full_page_match(g.TARGET)[0]
        #s_title = self.cont_sects[idx]["text"].get("1.0", tk.END)
        # title -> content -> repeat order
        for idx, sect in self.cont_sects.items():
            sect["tk"].update()
            newstring = sect["tk"].get("1.0", tk.END)
            if sect.get("title", "") != "":
                sect["title"] = newstring
                cont = g.MODELCTRL.update_content(g.TARGET_PAGE, sect)
            else:
                sect["content"] = newstring
                cont = g.MODELCTRL.update_content(g.TARGET_PAGE, sect)
        g.TARGET_PAGE_CONT = g.QUERY.page_content(g.TARGET_PAGE)

    def cancel(self):
        clear_colors()
        self.content.destroy()