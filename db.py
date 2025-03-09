import sqlite3 as sql
from sqlite3 import Connection

def connect(filename) -> Connection:
    return sql.connect(filename)
#TODO
def id_is_unique(id: int) -> bool:
    return True
#TODO
def get_full_name(id: int) -> (str, str, str):
    return (f"surname-{id}", "name", "last name")
#TODO
def add_pupil(pupil) -> None:
    print(pupil)
#TODO
def get_marks(id: int, subject: str) -> [(str, int)]:
    return [
        ("25.05", 13),
        ("18.02", 8),
    ]