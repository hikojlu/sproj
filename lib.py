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
    "Фізична культура",
])

def update_root_gui(con, table: ttk.Treeview):
    table.delete(*table.get_children())

    for id, *values in map((lambda x: x.right), con.get_pupils()):
        table.insert(
            parent="",
            index=tk.END,
            id=id,
            text=id,
            value=values
        )

def root_gui(con: db.Con):
    def delete_pupil(con: db.Con, table: ttk.Treeview) -> None:
        focus = table.focus()
        if not focus: return None
        con.delete_pupil(focus)
        update_root_gui(con,table)
    def edit_pupil(con: db.Con, table: ttk.Treeview) -> None:
        focus = table.focus()
    root = tk.Tk()
    root.geometry("1000x500")
    root.title("БД учнів")

    pupils_table = ttk.Treeview(root, columns=COLUMNS.left[1:])
    for i, (col, display) in enumerate(COLUMNS.all):
        pupils_table.heading(
            "#0" if i == 0 else col,
            text=display,
        )

    update_root_gui(con, pupils_table)

    add_button = tk.Button(root, text="Додати учня", command=lambda: add_pupil_gui(con, pupils_table))
    marks_button = tk.Button(root, text="Оцінки", command=lambda: marks_gui(con, pupils_table))
    rating_button = tk.Button(root, text="Успішність", command=lambda: rating_gui(con))
    delete_button = tk.Button(root, text="Видалити учня", command = lambda: delete_pupil(con, pupils_table))
    pupils_table.place(relx=0.25, rely=0.05, relwidth=0.7, relheight=0.8)
    add_button.place(relx=0.02, rely=0.1, relwidth=0.21, relheight=0.1)
    marks_button.place(relx=0.02, rely=0.4, relwidth=0.21, relheight=0.1)
    rating_button.place(relx=0.02, rely=0.55, relwidth=0.21, relheight=0.1)
    delete_button.place(relx=0.02, rely=0.25, relwidth=0.21, relheight=0.1)

    root.mainloop()
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
            ( "Некоректний номер учня",
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

        inputs = Columns([(col, e.get().strip()) for col, e in entries])

        q: bool = False
        for (err_msg, valid), (col, _input) in zip(inputs_tests, inputs.all):
            if not valid(_input):
                if err_msg == "Некоректний номер учня" and _input.isdigit():
                    q = messagebox.askyesno("Учень з таким номером уже існує", "Учень з таким номером уже існує, замінити його?")
                else:
                    messagebox.showerror(f"Помилка у `{col}`", err_msg)
                    return None
        if q:
            con.update_pupil(inputs.right[0], inputs.right[1:])
        else:
            con.add_pupil(inputs)
        update_root_gui(con, table)

        for _, e in entries:
            e.delete(0, 'end')

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
    focus = table.focus()
    if not focus:
        return None
    
    pupil = { "id": table.item(focus)["text"] } | table.set(focus)

    CURSUBJECT = None

    MARKS_COLUMNS = Columns([
        ("date", "Дата"),
        ("mark", "Оцінка"),
    ])

    def choose(subject: str):
        nonlocal CURSUBJECT
        CURSUBJECT = subject
        update_gui()
    def update_gui() -> None:
        subject = CURSUBJECT

        if not subject:
            return None

        add_mark_button.config(state="normal")
        delete_mark_button.config(state="normal")
        gen_label.config(text=f"Оцінки учня\n{pupil["surname"]} {pupil["name"]} {pupil["last_name"]}\nз {subject}")
        gui.title(f"Оцінки учня {pupil["surname"]} {pupil["name"]} {pupil["last_name"]} з {subject}")

        marks.delete(*marks.get_children())

        data = con.get_marks(int(pupil["id"]), subject)
        for date, mark in data.all:
            marks.insert(
                parent="",
                index=tk.END,
                text=date,
                values=(mark,)
            )
    def save(date, mark) -> None:
        con.add_mark(pupil["id"], CURSUBJECT, date, mark)
        update_gui()
    def delete(date, mark) -> None:
        con.delete_mark(int(pupil["id"]), CURSUBJECT, date, mark)
        update_gui()
    def exit() -> None:
        gui.destroy()

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
    marks.place(relx=0.7, rely=0.05, relwidth=0.25, relheight=0.9)
    
    subject_listbox = tk.Listbox(gui, selectmode="single",)
    subject_listbox.insert(tk.END, *SUBJECTS)
    subject_listbox.bind("<<ListboxSelect>>", lambda _: choose(SUBJECTS[subject_listbox.curselection()[0]]))
    subject_listbox.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.9)
    
    gen_label = tk.Label(gui, 
        text=f"Додати оцінки для:\n{pupil["surname"]} {pupil["name"]} {pupil["last_name"]}"
    )
    gen_label.place(relx=0.3, rely=0.05, relwidth=0.3, relheight=0.2)
    
    tk.Label(gui, text="Дата").place(relx=0.3, rely=0.3, relwidth=0.14, relheight=0.1)
    tk.Label(gui, text="Оцінка").place(relx=0.3, rely=0.42, relwidth=0.14, relheight=0.1)

    date_entry = tk.Entry(gui)
    date_entry.place(relx=0.45, rely=0.3, relwidth=0.14, relheight=0.1)

    mark_entry = tk.Entry(gui)
    mark_entry.place(relx=0.45, rely=0.42, relwidth=0.14, relheight=0.1)

    add_mark_button = tk.Button(gui, text="Додати таку оцінку", 
        command=lambda: save(date_entry.get(), mark_entry.get()), 
        state="disabled"
    )
    add_mark_button.place(relx=0.3, rely=0.53, relwidth=0.3, relheight=0.1)
    delete_mark_button = tk.Button(gui, text="Видалити оцінку", 
        command=lambda: delete(date_entry.get(), mark_entry.get()), 
        state="disabled"
    )
    delete_mark_button.place(relx=0.3, rely=0.65, relwidth=0.3, relheight=0.1)
    
    gui.mainloop()

def rating_gui(con: db.Con) -> None:
    def load(subject: str, sort: bool) -> None:
        table.delete(*table.get_children())
        data: [(int, str, int)] = []
        for id in con.get_all_ids():
            marks = con.get_marks(id, subject).right
            name = " ".join(con.get_name(id))
            try:
                avg = sum(marks) / len(marks)
            except ZeroDivisionError:
                continue
            data.append((id, name, avg))

        if sort:
            data.sort(key=(lambda x: x[2]), reverse=True)

        for id, name, mark in data:
            table.insert(
                parent="",
                index=tk.END,
                text=id,
                values=(name, f"{mark:.2f}")
            )

    gui = tk.Tk()
    gui.title("Успішність")
    gui.geometry("1000x470")
    gui.resizable(False, False)

    columns = Columns([
        ("id", "№"),
        ("full_name", "Повне ім'я"),
        ("avg", "Середня оцінка")
    ])

    table = ttk.Treeview(gui, columns=columns.left[1:])
    for i, (col, display) in enumerate(columns.all):
        table.heading(
            "#0" if i == 0 else col,
            text=display,
        )
    table.place(relx=0.25, rely=0.05, relwidth=0.72, relheight=0.92)

    subject_listbox = tk.Listbox(gui, selectmode="single")
    subject_listbox.insert(tk.END, *SUBJECTS)
    subject_listbox.place(relx=0.02, rely=0.05, relwidth=0.2, relheight=0.6)

    load_subject_button = tk.Button(gui, text="Обрати", 
        command=lambda: load(SUBJECTS[subject_listbox.curselection()[0]], sort=sort_var.get()))
    load_subject_button.place(relx=0.02, rely=0.66, relwidth=0.2, relheight=0.1)

    sort_var = tk.IntVar(gui, value=0)
    sort_cb = tk.Checkbutton(gui, text='Сортувати', variable=sort_var, onvalue=1, offvalue=0)
    sort_cb.place(relx=0.02, rely=0.8, relwidth=0.2, relheight=0.1)

    gui.mainloop()
    