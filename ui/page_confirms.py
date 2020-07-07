#!/usr/bin/env python3
import tkinter as tk
from ui.tk_helper import place
import ui.settings as s
from tkinter.filedialog import askopenfilename
import ui.language as en
import utils.globals as g


class DelConfirmPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=18)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.target = None
        self.check_target()

    def check_target(self):
        if g.TARGET and g.TARGET != "":
            self.target = g.TARGET
            self.selection()
        else:
            self.no_selection()

    def selection(self):
        message = f"{en.CONFIRM_1} {self.target}?"
        message_label = tk.Label(self.content, text=message)
        message_label.pack()
        self.buttons()

    def no_selection(self):
        message_label = tk.Label(self.content, text=en.CONFIRM_ERR_1, bg=s.FG,
                                 fg=s.SEARCHFG, font=(s.FONT2, 14, "bold"))
        place(message_label, h=1, w=1, x=0, y=0)

    def back(self):
        self.content.destroy()

    def buttons(self):
        self.yes = tk.Button(self.content, text="Yes", command=lambda: self.delete_target())
        self.yes.pack()
        self.no = tk.Button(self.content, text="No", command=lambda: self.back())
        self.no.pack()

if __name__ == "__main__":
    pass
