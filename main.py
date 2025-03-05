import os
import sqlite3 as sql
import tkinter as tk
from tkinter import ttk

DB_NAME = "pupils.sql"
COLUMNS = [
    ("id", "Номер учня"),
    ("surname", "Прізвище"),
    ("name", "Ім'я"),
    ("last_name", "По батькові"),
    ("class_number", "Клас"),
    ("class_letter", "Паралель")
]

if not os.path.exists(DB_NAME):
    with open(DB_NAME, 'w') as file:
        file.write("")

db = sql.connect(DB_NAME)
cur = db.cursor()

root = tk.Tk()
root.geometry("700x500")
root.title("hey")

testtw = ttk.Treeview(root, 
    columns=[e[0] for e in COLUMNS[1:]])

for i, col in enumerate(COLUMNS):
    testtw.heading("#0" if i == 0 else col[0],
        text=col[1])

data = cur.execute("""
    SELECT id, surname, name, last_name, class_number, class_letter FROM pupils ORDER BY id
""")
for row in data:
    testtw.insert(
        "",
        tk.END,
        text=row[0],
        values=row[1:]
    )

testtw.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.6)

root.mainloop()
