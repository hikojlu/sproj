class Columns:
    def __init__(self, columns: [(str, str)]):
        self.all = columns
        self.dict = { left: right for left, right in self.all}
        self.left = [e[0] for e in columns]
        self.right = [e[1] for e in columns]
        self.len = len(columns)