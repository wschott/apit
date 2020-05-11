class Song:
    def __init__(self, item):
        self.fields = item

    def __getitem__(self, field):
        return self.fields[field]
