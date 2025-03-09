import sqlite3 as sql
from sqlite3 import Connection

def id_is_unique(id: int) -> bool:
    return True

def add_pupil(pupil) -> None:
    print(pupil)

def connect(filename) -> Connection:
    print(filename)

def get_marks(id: int, subject: str) -> [(str, int)]:
    print(id, subject)
    return [
        ("25.05", 13),
        ("18.02", 8),
    ]