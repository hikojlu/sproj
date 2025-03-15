import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import db
from columns import Columns, COLUMNS

SUBJECTS = sorted([
    "Українська мова",
    "Українська література",
    "Зарубіжна література",
    "Історія України",
    "Всесвітня історія",
    "Іноземна мова",
    "Алгебра",
    "Геометрія",
    "Фізика",
    "Біологія",
    "Хімія",
    "Географія",
    "Основи правознавства",
    "Основи здоров'я",
    "Мистецтво",
    "Інформатика",
    "Технології",
    "Фіична культура",
])

def select_db_gui() -> str:
    filename = "foobar.db"
    def q() -> str:
        nonlocal filename
        filename = filedialog.askopenfilename()
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

    return filename
def add_pupil_gui(con: db.Con, table: ttk.Treeview) -> None:
    def save() -> None:
        cyrillic = set("йцукенгшщзхїфівапролджєячсмитьбюЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ-")
        inputs_tests = [
            ( "Уведіть існуючий, доступний, коректний номер",
                lambda id:
                    id.isdigit()
                    and con.id_is_unique(int(id))
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

        con.add_pupil(Columns(inputs))
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
def marks_gui(con: db.Con, table: ttk.Treeview) -> None:
    CURSUBJECT = None
    def choose(subject: str):
        nonlocal CURSUBJECT
        CURSUBJECT = subject
        def load_subject(subject: str) -> None:
            marks.delete(*marks.get_children())

            data = con.get_marks(int(pupil["id"]), subject)
            for date, mark in data.all:
                marks.insert(
                    parent="",
                    index=tk.END,
                    text=date,
                    values=(mark,)
                )
        def _choose(subject: str) -> None:
            add_marks_button.config(state="normal")
            gen_label.config(text=f"Оцінки учня\n{pupil["surname"]} {pupil["name"]} {pupil["last_name"]}\nз {subject}")
            gui.title(f"Оцінки учня {pupil["surname"]} {pupil["name"]} {pupil["last_name"]} з {subject}")
        load_subject(subject)
        _choose(subject)
    def save(data: Columns) -> None:
        con.add_mark(pupil["id"], CURSUBJECT, data.left[0], data.right[0])
        for date, mark in data.all:
                marks.insert(
                    parent="",
                    index=tk.END,
                    text=date,
                    values=(mark,)
                )     
    def exit() -> None:
        gui.destroy()

    focus = table.focus()
    if not focus:
        return None

    MARKS_COLUMNS = Columns([
        ("date", "Дата"),
        ("mark", "Оцінка"),
    ])

    pupil = { "id": table.item(focus)["text"] } | table.set(focus)

    gui = tk.Tk()
    gui.title(f"Оцінки учня {pupil["surname"]} {pupil["name"]} {pupil["last_name"]} з <предмет не обрано>")
    gui.geometry("1000x470")
    gui.resizable(False, False)

    marks = ttk.Treeview(gui, columns=MARKS_COLUMNS.left[1:])
    for i, (col, display) in enumerate(MARKS_COLUMNS.all):
        marks.heading(
            "#0" if i == 0 else col,
            text=display,
        )

    done_button = tk.Button(gui, text="Завершити", command=exit)
    
    subject_listbox = tk.Listbox(gui, selectmode="single")
    subject_listbox.insert(tk.END, *SUBJECTS)
    load_subject_button = tk.Button(gui, text="Обрати", 
        command=lambda: choose(SUBJECTS[subject_listbox.curselection()[0]]))
    
    gen_label = tk.Label(gui, text=f"Додати оцінки для:\n{pupil["surname"]} {pupil["name"]} {pupil["last_name"]}")

    date_label = tk.Label(gui, text="Дата")
    mark_label = tk.Label(gui, text="Оцінка")

    date_entry = tk.Entry(gui)
    mark_entry = tk.Entry(gui)

    add_marks_button = tk.Button(gui, text="Додати", 
        command=lambda: save(Columns([(date_entry.get(), mark_entry.get())])), state="disabled")

    gen_label.place(relx=0.3, rely=0.05, relwidth=0.3, relheight=0.2)
    date_label.place(relx=0.3, rely=0.3, relwidth=0.14, relheight=0.1)
    date_entry.place(relx=0.45, rely=0.3, relwidth=0.14, relheight=0.1)
    mark_label.place(relx=0.3, rely=0.42, relwidth=0.14, relheight=0.1)
    mark_entry.place(relx=0.45, rely=0.42, relwidth=0.14, relheight=0.1)
    add_marks_button.place(relx=0.3, rely=0.53, relwidth=0.3, relheight=0.1)

    marks.place(relx=0.7, rely=0.05, relwidth=0.25, relheight=0.75)
    done_button.place(relx=0.75, rely=0.82, relwidth=0.2, relheight=0.1)

    subject_listbox.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.75)
    load_subject_button.place(relx=0.05, rely=0.82, relwidth=0.2, relheight=0.1)
    
    gui.mainloop()
def rating_gui(con: db.Con) -> None:
    gui = tk.Tk()
    gui.title("Успішність")
    gui.geometry("1000x470")
    gui.resizable(False, False)

    ttk.Treeview(gui, columns=())

    gui.mainloop()

