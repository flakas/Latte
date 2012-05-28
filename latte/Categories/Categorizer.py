class Categorizer:
    categories = []

    def __init__(self, categories):
        self.categories = categories

    def categorize(self, window):
        for i in self.categories:
            if i.belongs(window):
                return i
        return None
