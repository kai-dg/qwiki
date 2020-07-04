#!/usr/bin/env python3
"""Add page button frame"""
import tkinter as tk
import ui.settings as s


def check_contents(data):
    """Data keys: page_name, header, contents"""
    if data["page_name"] == "":
        return False
    if data["header"] == "":
        return False
    return True

class AddPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FG, padx=18, pady=12)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        self.create_sections()
        self.single_inputs()
        self.buttons()
        self.text_and_display()

    def add_content(self, data):
        """Executing Add Content button."""
        self.errors["text"] = ""
        c = check_contents(data)
        if c:
            self.content_text.delete("1.0", tk.END)
            self.title.delete(0, "end")
            s.CONTENT[s.IDX] = {
                data["header"]: data["content"]
            }
            s.IDX += 1
            self.display["text"] += data["content"]
        else:
            self.errors["text"] = "ERROR: Page Name or Header is missing."

    def create_page(self):
        """Executing Create Page button. Resets global variables."""
        s.IDX = 0
        s.TARGET = 0
        s.CONTENT = {}
        s.PAGE_NAME = ""
        pass

    def get_inputs(self):
        name = self.name.get()
        content = self.content_text.get("1.0", tk.END)
        header = self.title.get()
        data = {
            "page_name": name,
            "header": header,
            "content": content
        }
        return data

    def text_and_display(self):
        self.content_text = tk.Text(self.middle, bg=s.SEARCHBG, font=(s.NORMAL_FONT, 9),
                                    fg=s.FG, padx=5, pady=5)
        self.content_text.place(relheight=0.7, relwidth=1, relx=0, rely=0.1)
        self.display = tk.Label(self.right_side, text="", wraplength=100, anchor="nw",
                                justify="left", padx=10, pady=10, bg=s.FG, fg=s.SEARCHBG)
        self.display.place(relheight=0.98, relwidth=0.98, relx=0.01, rely=0.01)
        self.errors = tk.Label(self.middle, text="", anchor="c", bg=s.FG,
                               fg=s.TEXT1, font=(s.NORMAL_FONT, 12, "bold"))
        self.errors.place(relwidth=1, relheight=0.05, relx=0, rely=0.885)

    def single_inputs(self):
        name_label = tk.Label(self.top, bg=s.FG, fg=s.TEXT1, text="Page Name:")
        name_label.place(relwidth=0.2, relx=0, rely=0.15)
        self.name = tk.Entry(self.top, bg=s.SEARCHFG, fg=s.FG, font=(s.NORMAL_FONT, 12))
        self.name.place(relwidth=0.68, relx=0.25, rely=0.15)
        content_title = tk.Label(self.middle, bg=s.FG, fg=s.TEXT1, text="Header:")
        content_title.place(relwidth=0.2, relx=0, rely=0.03)
        self.title = tk.Entry(self.middle, bg=s.SEARCHFG, fg=s.FG, font=(s.NORMAL_FONT, 12))
        self.title.place(relwidth=0.68, relx=0.25, rely=0.03)

    def buttons(self):
        add = tk.Button(self.middle, text="Add Content", font=(s.SEARCH_FONT, 9),
                           bg=s.SEARCHBG, fg=s.TEXT3, command=lambda: self.add_content(self.get_inputs()))
        add.place(relwidth=0.3, relx=0.33, rely=0.82)
        create = tk.Button(self.bottom, text="Create Page", font=(s.SEARCH_FONT, 9),
                           bg=s.SEARCHBG, fg=s.TEXT3)
        create.place(relwidth=0.3, relx=0.33, rely=0)

    def create_sections(self):
        self.top = tk.Frame(self.content, bg=s.FG)
        self.top.place(relheight=0.05, relwidth=0.5, relx=0, rely=0)
        self.middle = tk.Frame(self.content, bg=s.FG)
        self.middle.place(relheight=0.92, relwidth=0.5, relx=0, rely=0.05)
        self.bottom = tk.Frame(self.content, bg=s.FG)
        self.bottom.place(relheight=0.05, relwidth=0.5, relx=0, rely=0.93)
        self.right_side = tk.Frame(self.content, bg=s.FG)
        self.right_side.place(relheight=1, relwidth=0.5, relx=0.5, rely=0)
