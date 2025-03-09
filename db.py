import sqlite3 as sql
from sqlite3 import Connection
from columns import Columns

def connect(filename) -> Connection:
    return sql.connect(filename)
#TODO
def id_is_unique(id: int) -> bool:
    return True

#TODO
def add_pupil(pupil: Columns) -> None:
    print(pupil.dict)
#TODO
def add_mark(pupil_id: int, date: str, mark: str) -> None:
    print(pupil, date, mark)

#TODO
def get_marks(pupil_id: int, subject: str) -> [(str, int)]:
    return [
        ("25.05", 13),
        ("18.02", 8),
    ]