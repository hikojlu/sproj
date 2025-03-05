import tkinter as tk

#relx rely relwidth relheight
root = tk.Tk()

root.geometry('500x500')

test = tk.Label(text = 'test')
test.place(relx=0.1,rely=0.1,relwidth=0.5,relheight=0.2)

root.mainloop()
