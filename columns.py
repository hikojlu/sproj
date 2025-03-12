from typing import Any
class Columns:
    def __init__(self, columns: [(Any, Any)]):
        self.all = columns
        self.dict = { left: right for left, right in self.all }
        self.left = [e[0] for e in columns]
        self.right = [e[1] for e in columns]
        self.len = len(columns)
COLUMNS = Columns([
    ("id", "№"),
    ("surname", "Прізвище"),
    ("name", "Ім'я"),
    ("last_name", "По батькові"),
])
