import os
import sqlite3 as sql
import tkinter as tk
from tkinter import ttk

from lib import ColumnsWrapper

DB_NAME = "pupils.sql"
COLUMNS = ColumnsWrapper(
    ("id", "№"),
    ("surname", "Прізвище"),
    ("name", "Ім'я"),
    ("last_name", "По батькові"),
    ("class_number", "Клас"),
    ("class_letter", "Паралель"),
)

def insert_to_db_gui(db: sql.Connection) -> None:
    def save(entries: list[(str, tk.Entry)]) -> None:
        data = [(col, e.get()) for col, e in entries]
        # sqlite3 package docs recomend using 
        # `cur.executemany("INSERT INTO table VALUES(?, ?, <...>, ?)", (value, value, <...>, value))`
        # instead of f-strings to avoid sql injections
        db.cursor().executemany(f"""
                INSERT INTO pupils VALUES({", ".join(["?" for _ in COLUMNS.len]) })
            """, 
            data
        )
        gui.destroy()
            
    gui = tk.Tk()
    gui.title("Додати учня у таблицю")
    gui.geometry("250x300")
    gui.resizable(False, False)

    entries = []
    for place_mod, (col, display)  in enumerate(COLUMNS.all, 1):
        col_label = tk.Label(gui, text=display)
        entry = tk.Entry(gui)

        col_label.place(relx=0.05, rely=0.1 * place_mod, relwidth=0.3, relheight=0.1)
        entry.place(relx=0.35, rely=0.1 * place_mod, relwidth=0.6, relheight=0.1)

        entries.append((col, entry))

    done_button = tk.Button(gui, text="Додати", command=lambda: save(entries))
    cancel_button = tk.Button(gui, text="Відмінити", command=lambda: gui.destroy())

    done_button.place(relx=0.55, rely=0.75, relwidth=0.35, relheight=0.15)
    cancel_button.place(relx=0.1, rely=0.75, relwidth=0.35, relheight=0.15)
    
    gui.mainloop()

if not os.path.exists(DB_NAME):
    with open(DB_NAME, 'w') as file:
        file.write("")
        sql.connect(DB_NAME).cursor().execute(f"""
            CREATE TABLE pupils({", ".join(COLUMNS.ids)})
        """)

db = sql.connect(DB_NAME)
cur = db.cursor()

root = tk.Tk()
root.geometry("700x500")
root.title("hey")

pupils_treeview = ttk.Treeview(root, 
    columns=COLUMNS.ids[1:])

for i, col in enumerate(COLUMNS.all):
    pupils_treeview.heading("#0" if i == 0 else col[0],
        text=col[1])

data = cur.execute(f"""
    SELECT {", ".join(COLUMNS.ids)} FROM pupils ORDER BY id
""")
for i, row in enumerate(data):
    id = pupils_treeview.insert(
        "",
        tk.END,
        iid=i,
        text=row[0],
        values=row[1:]
    )

pupils_treeview.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.6)

add_button = tk.Button(root, text='Додати учня', command=lambda: insert_to_db_gui(db))
add_button.place(relx=0.05,rely=0.66,relwidth=0.15,relheight=0.1)

root.mainloop()
