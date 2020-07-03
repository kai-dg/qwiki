#!/usr/bin/env python3
import tkinter as tk

def app():
    root = tk.Tk()
    canvas = tk.Canvas(root, height=700, width=700, bg="#373634")
    canvas.pack()

    frame = tk.Frame(root, bg="white")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
    root.mainloop()

if __name__ == "__main__":
    pass
