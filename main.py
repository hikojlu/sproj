import os
import sqlite3 as sql
import tkinter as tk
from tkinter import ttk

DB_NAME = "pupils.sql"

if not os.path.exists(DB_NAME):
    with open(DB_NAME, 'w') as file:
        file.write("")

db = sql.connect(DB_NAME)
cur = db.cursor()

root = tk.Tk()
root.geometry("700x500")
root.title("hey")

testtw = ttk.Treeview(root, columns=("class_number", "class_letter"))
testtw.heading("#0", text="Прізвище, Ім'я",)
testtw.heading("class_number", text="Клас")
testtw.heading("class_letter", text="Клас (літера)")

data = cur.execute("""
    SELECT full_name, class_number, class_letter FROM pupils ORDER BY full_name
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
