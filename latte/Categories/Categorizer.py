import sys
import os
import inspect

from Category import Category

class Categorizer(object):
    categories = []

    def __init__(self, configs):
        self._configs = configs

    def categorize(self, window):
        for i in self.categories:
            if i.belongs(window):
                return i
        return None

    def loadCategories(self):
        path = os.path.join(self._configs['appPath'])
        if os.path.exists(path):
            sys.path.append(path)
            try:
                import categories
                for name, obj in inspect.getmembers(categories):
                    if inspect.isclass(obj) and obj.__module__ == 'categories':
                        self.addCategory(obj)
            except Exception as ex:
                print 'Cannot properly load categories'
                print ex
                pass

    def addCategory(self, category):
        if issubclass(category, Category):
            self.categories.append(category())
