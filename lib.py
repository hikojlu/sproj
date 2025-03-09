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
        global bd_connection
        filename = filedialog.askopenfilename()
        bd_connection = db.connect(filename)
        continue_button.config(state="normal")

        return filename

    bd_connection = None 
    
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

    return bd_connection

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
            # ( "Номер класу має бути числом між 1 і 11",
            #     lambda class_number:
            #         class_number.isdigit() 
            #         and (1 <= int(class_number) <= 11)
            # ),
            # ( "Паралель має бути одною великою буквою",
            #     lambda class_letter:
            #         len(class_letter) == 1 
            #         and class_letter in "ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ"
            # ),
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
    def choose(subject: str) -> None:
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

    pupil = { 
        "id": table.item(focus)["text"]
    } | table.set(focus)
    print(pupil)

    gui = tk.Tk()
    gui.title(f"Оцінки учня {focus}")
    gui.geometry("400x500")
    gui.resizable(False, False)

    marks = ttk.Treeview(gui, columns=MARKS_COLUMNS.left[1:])
    for i, (col, display) in enumerate(MARKS_COLUMNS.all):
        marks.heading(
            "#0" if i == 0 else col,
            text=display,
        )

    save_button = tk.Button(gui, text="Завершити")
    cancel_button = tk.Button(gui, text="Відмінити", command=exit)
    
    subject_listbox = tk.Listbox(gui, selectmode="single")
    subject_listbox.insert(tk.END, *SUBJECTS)
    choose_subject = tk.Button(gui, text="Обрати", 
        command=lambda: choose(SUBJECTS[subject_listbox.curselection()[0]]))

    #тут треба ентрі і лейбли для ввода оцінок і дати, вписування цьой шляпи у `marks` і визвання неіснуючої функції на сейв у бд ++ лоад з бд при запуску цьой заулпи

    subject_listbox.place(relx=0.1, rely=0.09, relwidth=0.35, relheight=0.1)
    choose_subject.place(relx=0.55, rely=0.09, relwidth=0.35, relheight=0.1)

    marks.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)
    save_button.place(relx=0.55, rely=0.85, relwidth=0.35, relheight=0.1)
    cancel_button.place(relx=0.1, rely=0.85, relwidth=0.35, relheight=0.1)
    
    gui.mainloop()

global COLUMNS 
COLUMNS = Columns([
    ("id", "№"),
    ("surname", "Прізвище"),
    ("name", "Ім'я"),
    ("last_name", "По батькові"),
    # ("class_number", "Клас"),
    # ("class_letter", "Паралель"),
])
