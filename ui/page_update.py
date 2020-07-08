#!/usr/bin/env python3
"""Update Page button frame"""
import tkinter as tk
from ui.tk_helper import place
import ui.settings as s
from ui.tk_helper import change_button_color
from ui.tk_helper import clear_colors
import ui.language as en
import utils.globals as g


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

    def create_cont_sects(self, cont):
        data = {}
        idx = 0
        for i in cont:
            data[idx] = {"text": tk.Text, "idx": i.idx, "model": i}
            idx += 1
            data[idx] = {"text": tk.Text, "idx": i.idx, "model": i}
        return data

    def draw_selection(self):
        cont = g.TARGET_PAGE_CONT
        self.cont_sects = self.create_cont_sects(cont)
        row_amt = ((len(cont)*2) + 3)
        self.buttons(row_amt)
        for r in range(row_amt):
            self.base.grid_rowconfigure(r, weight=0)
        self.base.grid_columnconfigure(0, weight=1)
        self.title = tk.Text(self.base, relief="flat", wrap="word", bg=s.BG2, padx=15,
                        pady=10, fg=s.SEARCHBG, highlightthickness=1, height=1,
                        font=(s.FONT2, 25, "bold"), highlightbackground="black",
                        highlightcolor=s.SEARCHFG)
        self.title.insert(tk.INSERT, g.TARGET_PAGE.name.rstrip())
        self.title.grid(row=0, sticky="ewn", rowspan=1)
        self.notes = tk.Text(self.base, relief="flat", bg=s.BG2, padx=25,
                        pady=10, fg=s.SEARCHBG, highlightthickness=1, height=1,
                        font=(s.FONT2, 12, "italic"), highlightbackground="black",
                        highlightcolor=s.SEARCHFG)
        self.notes.insert(tk.INSERT, g.TARGET_PAGE.notes.rstrip())
        new_height = int(round(float(self.notes.index(tk.END))))
        self.notes.config(height=new_height)
        self.notes.grid(row=1, sticky="ewns", rowspan=1)
        row_idx = 2
        sect_idx = 0
        # TODO change loop to self.cont_sects instead of cont
        for c in cont:
            ctitle = self.cont_sects[sect_idx]["text"](self.base, relief="flat", wrap="word", bg=s.BG2,
                             padx=15, pady=10, highlightthickness=1, height=1, 
                             highlightcolor=s.SEARCHFG, fg=s.SEARCHBG, font=(
                             s.FONT2,15, "bold"), highlightbackground="black")
            ctitle.insert(tk.INSERT, c.title)
            ctitle.grid(row=row_idx, sticky="ewns", rowspan=1)
            self.cont_sects[sect_idx]["text"] = ctitle
            # bind click to changing font color
            content = self.cont_sects[sect_idx+1]["text"](self.base, relief="flat", wrap="word", bg=s.BG2,
                              padx=24, pady=10,  highlightbackground="black",
                              fg=s.SEARCHBG, highlightthickness=1, height=5,
                              highlightcolor=s.SEARCHFG, font=(s.FONT2, 11))
            content.insert(tk.INSERT, c.content.rstrip())
            new_height = int(round(float(content.index(tk.END))))
            content.config(height=new_height)
            content.grid(row=(row_idx+1), sticky="ewns", rowspan=1)
            self.cont_sects[sect_idx+1]["text"] = content
            row_idx += 2
            sect_idx += 2

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
        #s_title = self.cont_sects[idx]["text"].get("1.0", tk.END)
        # title -> content -> repeat order
        is_title = False
        for sect in self.cont_sects.values():
            oldstring = sect["text"].get("1.0", tk.END)
            sect["text"].update()
            newstring = sect["text"].get("1.0", tk.END)
            if is_title:
                if oldstring != sect["model"].title:
                    m_update = sect["model"].update(title=newstring)
                    m_update.execute()
            else:
                if oldstring != sect["model"].content:
                    m_update = sect["model"].update(content=newstring)
                    m_update.execute()
        self.title.update()
        self.notes.update()

    def cancel(self):
        clear_colors()
        self.content.destroy()