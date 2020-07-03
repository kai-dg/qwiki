#!/usr/bin/env python3
import tkinter as tk
import ui.settings as s

def search_button():
    print("searching: ")
    return {}

def app():
    root = tk.Tk()
    root.title(s.TITLE)

    canvas = tk.Canvas(root, height=s.W_HEIGHT, width=s.W_WIDTH, bg=s.BACKGROUND)
    canvas.pack(fill="both", expand=True, padx=10, pady=20)

    frame = tk.Frame(canvas, bg=s.FOREGROUND)
    frame.place(relheight=0.95, relwidth=0.95, relx=0.5, rely=0.5, anchor="c")

    # Search bar frame
    frame_search = tk.Frame(frame, bg=s.SEARCHBARBG)
    frame_search.place(relx=0.1, rely=0, relheight=0.04, relwidth=2, anchor="n")
    searchlabel = tk.Label(frame_search, text="Name:", bg=s.SEARCHBARBG)
    searchlabel.config(font=(s.SEARCH_FONT, 9))
    searchlabel.place(relx=0.45, rely=0, relwidth=0.08, relheight=1)
    searchbar = tk.Entry(frame_search, font=(s.NORMAL_FONT, 12), bg=s.SEARCHBARFG)
    searchbar.place(relx=0.53, rely=0, relwidth=0.34, relheight=1)
    searchbutton = tk.Button(frame_search, text="SEARCH", font=(s.NORMAL_FONT, 9),
                             bg=s.BUTTON_D, fg=s.TEXT1, activebackground=s.BUTTON_A,
                             activeforeground=s.TEXT2,
                             command=lambda: search_button(searchbar.get()))
    searchbutton.place(relx=0.87, rely=0, relwidth=0.08, relheight=1)

    # Page frame
    frame_page = tk.Frame(frame, bg=s.FOREGROUND)
    frame_page.place(relheight=0.93, relwidth=1, relx=0.5, rely=0.04, anchor="n")

    # Editor frame
    frame_editor = tk.Frame(frame, bg="red")
    frame_editor.place(relheight=0.03, relwidth=1, relx=0.5, rely=1, anchor="s")
    add_wiki = tk.Button(frame_editor, text="Add Page", font=(s.SEARCH_FONT, 9))
    add_wiki.place(relwidth=0.25, relheight=1)
    update_wiki = tk.Button(frame_editor, text="Update Page", font=(s.SEARCH_FONT, 9))
    update_wiki.place(relx=0.25, relwidth=0.25, relheight=1)
    delete_wiki = tk.Button(frame_editor, text="Delete Page", font=(s.SEARCH_FONT, 9))
    delete_wiki.place(relx=0.5, relwidth=0.25, relheight=1)
    change_wiki = tk.Button(frame_editor, text="Change Wiki", font=(s.SEARCH_FONT, 9))
    change_wiki.place(relx=0.75, relwidth=0.25, relheight=1)

    root.mainloop()

if __name__ == "__main__":
    pass
