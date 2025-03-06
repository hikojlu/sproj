class ColumnsWrapper:
    def __init__(self, *columns: (str, str)):
        self.all = columns
        self.ids = [e[0] for e in columns]
        self.displays = [e[1] for e in columns]
        self.len = len(columns)