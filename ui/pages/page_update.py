#!/usr/bin/env python3
"""Update Page button frame"""
import tkinter as tk
from ui.tk_helper import place
import ui.settings as s
from ui.tk_helper import change_button_color
from ui.tk_helper import clear_colors
from ui.tk_helper import display_page
from ui.tk_styles import UpdatePageStyles
import ui.language as en
import utils.globals as g
from utils.models import set_ctrl


class UpdatePage(tk.Frame):
    def __init__(self, parent, button):
        change_button_color(button)
        tk.Frame.__init__(self, parent)
        self.base_f = tk.Frame(None)
        self.max_rows = 0
        place(self.base_f, h=0.93, w=1, x=0, y=0.04)
        self.styles = UpdatePageStyles(self)
        self.check_target()

    def check_target(self):
        if g.TARGET_PAGE and g.TARGET != "":
            self.selection()
        else:
            self.no_selection()

    def draw_scrollbar(self):
        self.base_f.bind("<Configure>", lambda e: self.canvas.configure(
                         scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.base_f, anchor="nw")
        self.scroll = tk.Scrollbar(self.canvas, orient="vertical",
                                   command=self.canvas.yview)
        self.scroll.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.
                             yview_scroll(int(-2*(event.delta/120)), "units"))

    def selection(self):
        self.base_f.destroy()
        self.canvas = tk.Canvas(None)
        place(self.canvas, h=0.93, w=1, x=0, y=0.04)
        self.base_f = tk.Frame(self.canvas)
        self.draw_scrollbar()
        display_page(self)
        self.styles.display_page(self)
        self.buttons()

    def no_selection(self):
        self.message_l = tk.Label(self.base_f)
        place(self.message_l, h=1, w=1, x=0, y=0)
        self.styles.no_selection(self)

    def buttons(self):
        self.button_f = tk.Frame(self.base_f, bg='red')
        self.button_f.grid(row=self.max_rows, sticky="ewns", columnspan=1)
        self.button_f.grid_columnconfigure(0, weight=0)
        self.button_f.grid_columnconfigure(1, weight=0)
        self.save_b = tk.Button(self.button_f, command=lambda: self.save())
        self.save_b.grid(row=0, column=0, sticky="ewns", padx=30, pady=20)
        self.cancel_b = tk.Button(self.button_f, command=lambda: self.cancel())
        self.cancel_b.grid(row=0, column=1, sticky="ewns", padx=30, pady=20)
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