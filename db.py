import sqlite3 as sql
from sqlite3 import Connection
from columns import Columns
from columns import COLUMNS
class Con:
    def __init__(self, o):
        self.con = sql.connect(o)
        self.path = o
        self.con.cursor().execute(
              """CREATE TABLE IF NOT EXISTS pupils
            (id INTEGER, surname TEXT, name TEXT, last_name TEXT)""")
        self.con.cursor().execute(
              """CREATE TABLE IF NOT EXISTS marks
            (id INTEGER, subject TEXT, date TEXT, mark INTEGER)""")

    def id_is_unique(self, id: int) -> bool:
        ids = self.con.cursor().execute("""SELECT id FROM pupils""").fetchall()
        ids = [int(e[0]) for e in ids]
        return not id in ids

    def add_pupil(self, pupil: Columns) -> None:
        self.con.cursor().execute(
            """INSERT INTO pupils (id, surname, name, last_name)
            VALUES (?,?,?,?)""", pupil.right)
        self.con.commit()

    def add_mark(self, pupil_id: int, subject: str, date: str, mark: str) -> None:
        self.con.cursor().execute("""
            INSERT INTO marks (id, subject, date, mark)
            VALUES (?,?,?,?)
        """, (pupil_id, subject, date, mark))
        self.con.commit()

    def get_all_ids(self) -> [int]:
        return [e[0] for e in self.con.cursor().execute("SELECT id FROM pupils").fetchall()]
    def get_pupils(self) -> list[Columns]:
        data = self.con.cursor().execute("SELECT * FROM pupils").fetchall()

        return [Columns([
            ("id", id),
            ("surname", surname),
            ("name", name),
            ("last_name", last_name),
        ]) for id, surname, name, last_name in data]
    def get_marks(self, pupil_id: int, subject: str) -> Columns:

        data = self.con.cursor().execute("""
            SELECT date, mark FROM marks WHERE id = ? AND subject = ?
        """, (pupil_id, subject)).fetchall()
        return Columns(data)
    def get_name(self, id: int) -> str:
        return (self.con.cursor().execute("SELECT surname, name, last_name FROM pupils WHERE id = ?", (id,)).fetchall()[0])
    
    def delete_val(self, tableName: str, id_name: str, val_name: str) -> None:
        self.con.cursor().execute(f"DELETE FROM {tableName} WHERE {id_name}= {val_name}")
        self.con.commit()
    def update_val(self, tableName: str, specifier: int | str, ids: tuple, values: tuple) -> None:
        com = ", ".join([f"{i} = ?" for i in ids])
        print(com)
        self.con.cursor().execute(f"UPDATE {tableName} SET {com} WHERE id = {specifier}", values)
        self.con.commit()
