#!/usr/bin/env python3
import tkinter as tk
import ui.settings as s
import utils.database as db
from ui.page_wiki import WikiPage
from ui.page_change_wiki import ChangeWikiPage
from ui.page_add import AddPage
from ui.page_update import UpdatePage
from ui.page_confirms import DelConfirmPage
s.WIKI_DB_INFO = db.read_json()
s.DEFAULT_DB = s.WIKI_DB_INFO["active"] if s.WIKI_DB_INFO["active"] != "" else s.DEFAULT_DB
s.WIKI_LIST = list(s.WIKI_DB_INFO["wikis"])
s.WIKI_LIST = [""] if s.WIKI_LIST == [] else s.WIKI_LIST


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(s.TITLE)
        self.root.geometry(f"{s.W_HEIGHT}x{s.W_WIDTH}")
        self.frame = tk.Frame(self.root, bg=s.FG)
        self.frame.place(relheight=1, relwidth=1, relx=0.5, rely=0.5, anchor="c")
        self.search_bar()
        self.content()
        self.bottom_buttons()
        self.root.mainloop()

    def replace(self, cls):
        """Controller for changing self.content frame"""
        self.content.destroy()

    def content(self):
        self.content = tk.Frame(self.frame, bg=s.FG)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        lab = tk.Label(self.content, text=s.WELCOME, font=(s.FONT1, 12, "bold"),
                       bg=s.FG, fg=s.SEARCHFG)
        lab.place(relheight=1, relwidth=1, relx=0, rely=0)

    def search_bar(self):
        frame_search = tk.Frame(self.frame, bg=s.SEARCHBG)
        frame_search.place(relx=0.1, rely=0, relheight=0.04, relwidth=2, anchor="n")
        self.searchlabel = tk.Label(frame_search, text=s.DEFAULT_DB, bg=s.SEARCHBG)
        self.searchlabel.config(font=(s.FONT1, 9, "bold"))
        self.searchlabel.place(relx=0.45, rely=0, relwidth=0.08, relheight=1)
        self.searchbar = tk.Entry(frame_search, font=(s.NORMAL_FONT, 12), bg=s.SEARCHFG,
                                  fg=s.TEXT2)
        self.searchbar.place(relx=0.53, rely=0, relwidth=0.34, relheight=1)
        searchbutton = tk.Button(frame_search, text="SEARCH", font=(s.NORMAL_FONT, 9),
                                 bg=s.BUTTON_D, fg=s.TEXT1, activebackground=s.BUTTON_A,
                                 activeforeground=s.TEXT2,
                                 command=lambda: self.replace(WikiPage(self.frame,
                                 self.searchbar.get())))
        searchbutton.place(relx=0.87, rely=0, relwidth=0.08, relheight=1)
        search_tag_b = tk.Button(frame_search, text="BY TAG")
        # place it

    def bottom_buttons(self):
        frame_editor = tk.Frame(self.frame, bg="red")
        frame_editor.place(relheight=0.03, relwidth=1, relx=0.5, rely=1, anchor="s")
        add_wiki = tk.Button(frame_editor, text="Add Page", font=(s.FONT1, 9),
                                    bg=s.SEARCHBG, fg=s.TEXT3,
                             command=lambda: self.replace(AddPage(self.frame)))
        add_wiki.place(relwidth=0.25, relheight=1)
        update_wiki = tk.Button(frame_editor, text="Update Page", font=(s.FONT1, 9),
                                    bg=s.SEARCHBG, fg=s.TEXT3,
                                command=lambda: self.replace(UpdatePage(self.frame)))
        update_wiki.place(relx=0.25, relwidth=0.25, relheight=1)
        delete_wiki = tk.Button(frame_editor, text="Delete Page", font=(s.FONT1, 9),
                                    bg=s.SEARCHBG, fg=s.TEXT3,
                                command=lambda: self.replace(DelConfirmPage(
                                self.frame)))
        delete_wiki.place(relx=0.5, relwidth=0.25, relheight=1)
        change_wiki = tk.Button(frame_editor, text="Wiki Settings", font=(s.FONT1, 9),
                                    bg=s.SEARCHBG, fg=s.TEXT3,
                                    command=lambda: self.replace(ChangeWikiPage(self.frame,
                                    self.searchlabel)))
        change_wiki.place(relx=0.75, relwidth=0.25, relheight=1)

if __name__ == "__main__":
    pass
