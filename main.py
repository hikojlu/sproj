from lib import *

CON = db.Con(select_db_gui())

root = tk.Tk()
root.geometry("1000x500")
root.title("БД учнів")

pupils_table = ttk.Treeview(root, columns=COLUMNS.left[1:])
for i, (col, display) in enumerate(COLUMNS.all):
    pupils_table.heading(
        "#0" if i == 0 else col,
        text=display,
    )

for pupil in CON.get_pupils():
    pupils_table.insert(
        parent="",
        index=tk.END,
        text=pupil.right[0],
        value=pupil.right[1:]
    )

add_button = tk.Button(root, text="Додати учня", command=lambda: add_pupil_gui(CON, pupils_table))
marks_button = tk.Button(root, text="Оцінки", command=lambda: marks_gui(CON, pupils_table))
rating_button = tk.Button(root, text="Успішність", command=lambda: rating_gui(CON))

pupils_table.place(relx=0.25, rely=0.05, relwidth=0.7, relheight=0.8)
add_button.place(relx=0.02, rely=0.1, relwidth=0.21, relheight=0.1)
marks_button.place(relx=0.02, rely=0.25, relwidth=0.21, relheight=0.1)
rating_button.place(relx=0.02, rely=0.4, relwidth=0.21, relheight=0.1)

root.mainloop()
