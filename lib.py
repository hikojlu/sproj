import tkinter as tk
import sqlite3 as sql
from tkinter import ttk

class Columns:
    def __init__(self, columns: [(str, str)]):
        self.all = columns
        self.ids = [e[0] for e in columns]
        self.displays = [e[1] for e in columns]
        self.len = len(columns)

class Table:
    def __init__(self, win: tk.Tk, columns: Columns, con: sql.Connection):
        self.win = win
        self.columns = columns
        self.tview = ttk.Treeview(win, columns=self.columns.ids)

        print(self.columns.all)
        for i, (col, display) in enumerate(self.columns.all):
            print(i, col, display)
            self.tview.heading(
                "#0" if i == 0 else col,
                text=display
            )

        data = con.cursor().execute(f"""
            SELECT {", ".join(self.columns.ids)} FROM pupils ORDER BY id
        """)
        for id, *rest in data:
            self.tview.insert(
                "",
                tk.END,
                iid=id,
                text=id,
                values=rest
            )
