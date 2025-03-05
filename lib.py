class Columns:
    def __init__(self, *columns):
        self.columns = columns
        self.ids = [e[0] for e in columns]
        self.displays = [e[1] for e in columns]