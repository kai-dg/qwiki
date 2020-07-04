#!/usr/bin/env python3
import tkinter as tk
import ui.settings as s

class AddPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FOREGROUND)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        lab2 = tk.Label(self.content, text="helloadd")
        lab2.pack()

class WikiTab(tk.Frame):
    def __init__(self, parent, entry):
        tk.Frame.__init__(self, parent)
        self.content = tk.Frame(parent, bg=s.FOREGROUND)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        text = tk.Text(self.content, width=50, bg=s.FOREGROUND, fg=s.SEARCHBARFG, font=(s.NORMAL_FONT, 11))
        text.place(relheight=1, relwidth=1, relx=0.5, rely=0, anchor="n")
        text.insert(tk.INSERT, entry)

class App3():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(s.TITLE)
        self.root.geometry(f"{s.W_HEIGHT}x{s.W_WIDTH}")
        self.frame = tk.Frame(self.root, bg=s.FOREGROUND)
        self.frame.place(relheight=1, relwidth=1, relx=0.5, rely=0.5, anchor="c")
        self.search_bar()
        self.content()
        self.bottom_buttons()
        self.root.mainloop()

    def replace(self, cls):
        self.content.destroy()

    def content(self):
        self.content = tk.Frame(self.frame, bg=s.FOREGROUND)
        self.content.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")
        lab = tk.Label(self.content, text=s.WELCOME, bg=s.FOREGROUND, fg=s.SEARCHBARFG)
        lab.place(relheight=1, relwidth=1, relx=0, rely=0)

    def search_bar(self):
        frame_search = tk.Frame(self.frame, bg=s.SEARCHBARBG)
        frame_search.place(relx=0.1, rely=0, relheight=0.04, relwidth=2, anchor="n")
        searchlabel = tk.Label(frame_search, text="Name:", bg=s.SEARCHBARBG)
        searchlabel.config(font=(s.SEARCH_FONT, 9))
        searchlabel.place(relx=0.45, rely=0, relwidth=0.08, relheight=1)
        self.searchbar = tk.Entry(frame_search, font=(s.NORMAL_FONT, 12), bg=s.SEARCHBARFG)
        self.searchbar.place(relx=0.53, rely=0, relwidth=0.34, relheight=1)
        searchbutton = tk.Button(frame_search, text="SEARCH", font=(s.NORMAL_FONT, 9),
                                 bg=s.BUTTON_D, fg=s.TEXT1, activebackground=s.BUTTON_A,
                                 activeforeground=s.TEXT2,
                                 command=lambda: self.replace(WikiTab(self.frame, self.searchbar.get())))
        searchbutton.place(relx=0.87, rely=0, relwidth=0.08, relheight=1)

    def bottom_buttons(self):
        frame_editor = tk.Frame(self.frame, bg="red")
        frame_editor.place(relheight=0.03, relwidth=1, relx=0.5, rely=1, anchor="s")
        add_wiki = tk.Button(frame_editor, text="Add Page", font=(s.SEARCH_FONT, 9),
                                    bg=s.SEARCHBARBG, fg=s.TEXT2,
                             command=lambda: self.replace(AddPage(self.frame)))
        add_wiki.place(relwidth=0.25, relheight=1)
        update_wiki = tk.Button(frame_editor, text="Update Page", font=(s.SEARCH_FONT, 9),
                                    bg=s.SEARCHBARBG, fg=s.TEXT2)
        update_wiki.place(relx=0.25, relwidth=0.25, relheight=1)
        delete_wiki = tk.Button(frame_editor, text="Delete Page", font=(s.SEARCH_FONT, 9),
                                    bg=s.SEARCHBARBG, fg=s.TEXT2)
        delete_wiki.place(relx=0.5, relwidth=0.25, relheight=1)
        change_wiki = tk.Button(frame_editor, text="Change Wiki", font=(s.SEARCH_FONT, 9),
                                    bg=s.SEARCHBARBG, fg=s.TEXT2)
        change_wiki.place(relx=0.75, relwidth=0.25, relheight=1)

if __name__ == "__main__":
    pass
