import sqlite3 as sql
from sqlite3 import Connection
from columns import Columns
class Con:
    def __init__(self, o):
        self.con = sql.connect(o)
    #TODO
    def id_is_unique(self, id: int) -> bool:
        print("id_is_unique", id)
        return True

    #TODO 
    def add_pupil(self, pupil: Columns) -> None:
        print("add_pupil", pupil.dict)
    #TODO #TODO
    def add_mark(self, pupil_id: int, subject: str, date: str, mark: str) -> None:
        print("add_mark", pupil, date, mark)

    #TODO
    def get_pupils(self) -> list[Columns]:
        return []
    #TODO
    def get_marks(self, pupil_id: int, subject: str) -> Columns:
        print("get_marks", pupil_id, subject)
        return Columns([
            ("25.05", 13),
            ("18.02", 8),
        ])