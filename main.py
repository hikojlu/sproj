from lib import *

con = select_db_gui()

root = tk.Tk()
root.geometry("1000x500")
root.title("БД учнів")

pupils_table = ttk.Treeview(root, columns=COLUMNS.left[1:])
for i, (col, display) in enumerate(COLUMNS.all):
    pupils_table.heading(
        "#0" if i == 0 else col,
        text=display,
    )

add_button = tk.Button(root, text="Додати учня", command=lambda: add_pupil_gui(pupils_table))
marks_button = tk.Button(root, text="Оцінки", command=lambda: marks_gui(pupils_table))

pupils_table.place(relx=0.25, rely=0.05, relwidth=0.7, relheight=0.8)
add_button.place(relx=0.02, rely=0.1, relwidth=0.21, relheight=0.1)
marks_button.place(relx=0.02, rely=0.25, relwidth=0.21, relheight=0.1)

root.mainloop()
