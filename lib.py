import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import db

class Columns:
    def __init__(self, columns: [(str, str)]):
        self.all = columns
        self.left = [e[0] for e in columns]
        self.right = [e[1] for e in columns]
        self.len = len(columns)
        self.dict = { left: right for left, right in self.all}
def select_db_gui() -> db.Connection:
    def q() -> str:
        global db_con
        filename = filedialog.askopenfilename()
        db_con = db.connect(filename)
        continue_button.config(state="normal")

        return filename
    
    gui = tk.Tk()
    gui.title("Відкрити базу даних")
    gui.geometry("400x200")
    gui.resizable(False, False)

    label = tk.Label(gui, text="БД не обрано")
    choose_button = tk.Button(gui, text="Обрати БД", command=lambda: label.config(text=q()))
    continue_button = tk.Button(gui, text="Продовжити", command=gui.destroy, state="disabled")

    label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)
    choose_button.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.3)
    continue_button.place(relx=0.6, rely=0.6, relwidth=0.3, relheight=0.3)

    gui.protocol("WM_DELETE_WINDOW", exit)
    gui.mainloop()

    return db_con
def add_pupil_gui(table: ttk.Treeview) -> None:
    def save() -> None:
        cyrillic = set("йцукенгшщзхїфівапролджєячсмитьбюЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ-")
        inputs_tests = [
            ( "Уведіть існуючий, доступний, коректний номер",
                lambda id:
                    id.isdigit()
                    and db.id_is_unique(int(id))
            ),    
            ( "Неможливо прочитати прізвище",
                lambda surname:
                    surname 
                    and set(surname).issubset(cyrillic)
            ),
            ( "Неможливо прочитати ім'я",
                lambda name:
                    name
                    and set(name).issubset(cyrillic) 
            ),
            ( "Неможливо прочитати ім'я по батькові",
                lambda last_name:
                    last_name
                    and set(last_name).issubset(cyrillic)
            ),
        ]

        inputs = [(col, e.get().strip()) for col, e in entries]

        for (err_msg, valid), (col, _input) in zip(inputs_tests, inputs):
            if not valid(_input):
                messagebox.showerror(f"Помикла у `{col}`", err_msg)
                return None

        db.add_pupil(inputs)
        write(table, Columns(inputs))
        exit()
    
    def write(tv: ttk.Treeview, data: Columns) -> None:
        tv.insert(
            parent="",
            index=tk.END,
            id=data.right[0],
            text=data.right[0],
            values=data.right[1:],
        )

    def exit() -> None:
        gui.destroy()
            
    gui = tk.Tk()
    gui.title("Додати учня у таблицю")
    gui.geometry("250x300")
    gui.resizable(False, False)

    entries: list[(str, tk.Entry)] = []
    for place_mod, (col, display) in enumerate(COLUMNS.all, 1):
        col_label = tk.Label(gui, text=display)
        entry = tk.Entry(gui)

        col_label.place(relx=0.05, rely=0.14 * place_mod, relwidth=0.3, relheight=0.1)
        entry.place(relx=0.35, rely=0.14 * place_mod, relwidth=0.6, relheight=0.1)

        entries.append((col, entry))

    done_button = tk.Button(gui, text="Додати", command=save)
    cancel_button = tk.Button(gui, text="Відмінити", command=exit)

    done_button.place(relx=0.55, rely=0.75, relwidth=0.35, relheight=0.15)
    cancel_button.place(relx=0.1, rely=0.75, relwidth=0.35, relheight=0.15)
    
    gui.mainloop()
def marks_gui(table: ttk.Treeview) -> None:
    def load_subject(subject: str) -> None:
        marks.delete(*marks.get_children())

        data = db.get_marks(int(pupil["id"]), subject)
        for date, mark in data:
            marks.insert(
                parent="",
                index=tk.END,
                text=date,
                values=(mark,)
            )
    def exit() -> None:
        gui.destroy()

    MARKS_COLUMNS = Columns([
        ("date", "Дата"),
        ("mark", "Оцінка"),
    ])
    SUBJECTS = [
        "Математика",
        "Українська мова",
        "Історія України",
    ]

    focus = table.focus()
    if not focus:
        return None

    pupil = { "id": table.item(focus)["text"] } | table.set(focus)


    gui = tk.Tk()#              >><< doesn't work
    gui.title(f"Оцінки учня {table.get_children()[int(focus[0])]}")
    gui.geometry("1000x500")
    gui.resizable(False, False)

    marks = ttk.Treeview(gui, columns=MARKS_COLUMNS.left[1:])
    for i, (col, display) in enumerate(MARKS_COLUMNS.all):
        marks.heading(
            "#0" if i == 0 else col,
            text=display,
        )

    save_button = tk.Button(gui, text="Завершити", command=exit)
    
    subject_listbox = tk.Listbox(gui, selectmode="single")
    subject_listbox.insert(tk.END, *SUBJECTS)
    load_subject_button = tk.Button(gui, text="Обрати", 
        command=lambda: load_subject(SUBJECTS[subject_listbox.curselection()[0]]))
    
    marks.place(relx=0.6, rely=0.05, relwidth=0.3, relheight=0.75)
    save_button.place(relx=0.6, rely=0.8, relwidth=0.3, relheight=0.1)

    subject_listbox.place(relx=0.05, rely=0.05, relwidth=0.3, relheight=0.75)
    load_subject_button.place(relx=0.05, rely=0.8, relwidth=0.3, relheight=0.1)
    
    gui.mainloop()

global COLUMNS 
COLUMNS = Columns([
    ("id", "№"),
    ("surname", "Прізвище"),
    ("name", "Ім'я"),
    ("last_name", "По батькові"),
])
