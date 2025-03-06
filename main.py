import os
import sqlite3 as sql
import tkinter as tk
from tkinter import ttk

from lib import ColumnsWrapper

def SaveDB(data):
    print(1)
    #cur.execute(f"INSERT INTO pupils ({koloni}) VALUES ({value})")

def AddGui():
    def save():
        data = []
        for x in entries:
            idd = x[0]; value = x[1].get()
            data.append((idd,value))
        print(data)
        #SaveDB(data)
        gui.destroy()
            
    gui = tk.Tk()
    gui.title("Додати учня у таблицю")
    gui.geometry("250x300"); gui.resizable(False,False)

    c = 1
    entries = []
    for i in COLUMNS.columns:
        lab = tk.Label(gui, text=i[1])
        lab.place(relx=0.05,rely=0.1*c,relwidth=0.3,relheight=0.1)
        entry = tk.Entry(gui)
        entry.place(relx=0.35,rely=0.1*c,relwidth=0.6,relheight=0.1)

        entries.append((i[0],entry))
        c+=1
    done = tk.Button(gui,text='Завершити',command=save)
    done.place(relx=0.35,rely=0.75,relwidth=0.35,relheight=0.15)
    
    gui.mainloop()

DB_NAME = "pupils.sql"
COLUMNS = ColumnsWrapper(
    ("id", "№"),
    ("surname", "Прізвище"),
    ("name", "Ім'я"),
    ("last_name", "По батькові"),
    ("class_number", "Клас"),
    ("class_letter", "Паралель"),
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

addButton = tk.Button(root, text='Додати учня', command=AddGui)
addButton.place(relx=0.05,rely=0.66,relwidth=0.15,relheight=0.1)

root.mainloop()
