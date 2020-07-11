#!/usr/bin/env python3
"""Update Page button frame"""
import tkinter as tk
from ui.tk_helper import place
import ui.settings as s
from ui.tk_helper import change_button_color
from ui.tk_helper import clear_colors
import ui.language as en
import utils.globals as g
from utils.models import set_ctrl


class UpdatePage(tk.Frame):
    def __init__(self, parent, button):
        change_button_color(button)
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG, padx=10, pady=10)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.check_target()

    def check_target(self):
        if g.TARGET_PAGE and g.TARGET != "":
            self.selection()
        else:
            self.no_selection()

    def selection(self):
        self.base = tk.Frame(self.content, bg=s.FG, padx=25, pady=25)
        place(self.base, h=1, w=1, x=0, y=0)
        self.draw_selection()

    def no_selection(self):
        message_label = tk.Label(self.content, text=en.UP_ERR_1, bg=s.FG,
                                 fg=s.SEARCHFG, font=(s.FONT2, 20, "bold"))
        place(message_label, h=1, w=1, x=0, y=0)

    def create_cont_sects(self):
        data = {}
        page_idx = 0
        for i in g.TARGET_PAGE_CONT:
            data[page_idx] = {"tk": tk.Text, "idx": i.idx, "title": i.title}
            page_idx += 1
            data[page_idx] = {"tk": tk.Text, "idx": i.idx, "content": i.content}
        return data

    def draw_selection(self):
        self.cont_sects = self.create_cont_sects()
        row_amt = ((len(list(self.cont_sects))) + 3)
        self.buttons(row_amt)
        for r in range(row_amt):
            self.base.grid_rowconfigure(r, weight=0)
        self.base.grid_columnconfigure(0, weight=1)
        self.title = tk.Text(self.base, relief="flat", wrap="word", bg=s.BG2, padx=15,
                        pady=10, fg=s.SEARCHBG, highlightthickness=1, height=1,
                        font=(s.FONT2, 25, "bold"), highlightbackground="black",
                        highlightcolor=s.SEARCHFG)
        self.title.insert(tk.INSERT, g.TARGET_PAGE.name)
        self.title.grid(row=0, sticky="ewn", rowspan=1)
        self.notes = tk.Text(self.base, relief="flat", bg=s.BG2, padx=25,
                        pady=10, fg=s.SEARCHBG, highlightthickness=1, height=1,
                        font=(s.FONT2, 12, "italic"), highlightbackground="black",
                        highlightcolor=s.SEARCHFG)
        self.notes.insert(tk.INSERT, g.TARGET_PAGE.notes)
        new_height = int(round(float(self.notes.index(tk.END))))
        self.notes.config(height=new_height)
        self.notes.grid(row=1, sticky="ewns", rowspan=1)
        for idx, data in self.cont_sects.items():
            if data.get("title", "") != "":
                ctitle = data["tk"](self.base, relief="flat", wrap="word", bg=s.BG2,
                                 padx=15, pady=10, highlightthickness=1, height=1, 
                                 highlightcolor=s.SEARCHFG, fg=s.SEARCHBG, font=(
                                 s.FONT2,15, "bold"), highlightbackground="black")
                ctitle.insert(tk.INSERT, data["title"])
                ctitle.grid(row=idx+2, sticky="ewns", rowspan=1)
                data["tk"] = ctitle
            else:
            # bind click to changing font color
                content = data["tk"](self.base, relief="flat", wrap="word", bg=s.BG2,
                                  padx=24, pady=10,  highlightbackground="black",
                                  fg=s.SEARCHBG, highlightthickness=1, height=5,
                                  highlightcolor=s.SEARCHFG, font=(s.FONT2, 11))
                content.insert(tk.INSERT, data["content"])
                new_height = int(round(float(content.index(tk.END))))
                content.config(height=new_height)
                content.grid(row=idx+2, sticky="ewns", rowspan=1)
                data["tk"] = content


    def buttons(self, row_idx):
        button_base = tk.Frame(self.base, bg=s.FG)
        button_base.grid(row=row_idx, sticky="ewns", rowspan=1)
        button_base.grid_columnconfigure(0, weight=1)
        button_base.grid_columnconfigure(1, weight=1)
        save = tk.Button(button_base, text=en.UP_B1, font=(s.FONT1, 10, "bold"),
                         bg=s.SEARCHBG, fg=s.TEXT3, command=lambda: self.save())
        save.grid(row=0, column=0, sticky="ewns", padx=10, pady=20)
        cancel = tk.Button(button_base, text=en.UP_B2, font=(s.FONT1, 10, "bold"),
                           bg=s.SEARCHBG, fg=s.TEXT3, command=lambda: self.cancel())
        cancel.grid(row=0, column=1, sticky="ewns", padx=10, pady=20)

    def save(self):
        """Updates self.cont_sects, self.title, and self.notes.
        Formats self.cont_sects into data for updating Content model.
        """
        data = {
            "name": self.title.get("1.0", tk.END),
            "notes": self.notes.get("1.0", tk.END)
        }
        if data["name"] != g.TARGET_PAGE.name:
            self.title.update()
            data["name"] = self.title.get("1.0", tk.END).rstrip().title()
            new_page = g.MODELCTRL.update_page(g.TARGET, data)
        if data["notes"] != g.TARGET_PAGE.notes:
            self.notes.update()
            data["notes"] = self.notes.get("1.0", tk.END).rstrip().capitalize()
            new_page = g.MODELCTRL.update_page(g.TARGET, data)
        g.TARGET = self.title.get("1.0", tk.END).rstrip().title()
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