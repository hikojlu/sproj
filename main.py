import os
import sqlite3 as sql
import tkinter as tk
from tkinter import ttk

from lib import Columns

DB_NAME = "pupils.sql"
COLUMNS = ColumnsWrapper(
    ("id", "№"),
    ("surname", "Прізвище"),
    ("name", "Ім'я"),
    ("last_name", "По батькові"),
    ("class_number", "Клас"),
    ("class_letter", "Паралель")
)

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

testtw = ttk.Treeview(root, 
    columns=COLUMNS.ids[1:])

for i, col in enumerate(COLUMNS.columns):
    testtw.heading("#0" if i == 0 else col[0],
        text=col[1])

data = cur.execute(f"""
    SELECT {", ".join(COLUMNS.ids)} FROM pupils ORDER BY id
""")
for i, row in enumerate(data):
    id = testtw.insert(
        "",
        tk.END,
        iid=i,
        text=row[0],
        values=row[1:]
    )

testtw.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.6)

root.mainloop()
