#!/usr/bin/env python3
import tkinter as tk
from ui.tk_helper import place
import ui.settings as s
from tkinter.filedialog import askopenfilename
import os

class DelConfirmPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=18)
        place(self.content, h=0.93, w=1, x=0.5, y=0.04, a="n")
        self.target = s.TARGET
        message = f"Are you sure you want to delete {self.target}?"
        message_label = tk.Label(self.content, text=message)
        message_label.pack()
        self.buttons()

    def delete_target(self):
        filename = askopenfilename()
        print(os.path.basename(filename))

    def back(self):
        self.content.destroy()

    def buttons(self):
        self.yes = tk.Button(self.content, text="Yes", command=lambda: self.delete_target())
        self.yes.pack()
        self.no = tk.Button(self.content, text="No", command=lambda: self.back())
        self.no.pack()

if __name__ == "__main__":
    pass
