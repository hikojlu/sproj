from tkinter import Tk
from tkinter.ttk import Treeview
from sqlite3 import Connection

class Columns:
    def __init__(self, columns: [(str, str)]):
        self.all = columns
        self.ids = [e[0] for e in columns]
        self.displays = [e[1] for e in columns]
        self.len = len(columns)

class Table:
    def __init__(self, win: Tk, columns: Columns):
        self.win = win
        self.columns = columns
        self.table = Treeview(win, columns=columns)
    def headings(self) -> None:
        #CRASHES! here at i=2
        for i, (col, display) in enumerate(self.columns.all):
            self.table.heading(
                "#0" if i == 0 else col,
                text=display
            )
    def load(self, db: Connection) -> None:
        data = db.cursor().execute(f"""
            SELECT {", ".join(self.columns.ids)} FROM pupils ORDER BY id
        """)
        for id, *rest in data:
            self.table.insert(
                "",
                tk.END,
                iid=id,
                text=id,
                values=rest
            )
