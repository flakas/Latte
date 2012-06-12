"""

Window categorization class.
Categorizes windows according to user-defined category classes

"""
import sys
import os
import inspect

from latte.Categories.Category import Category

class Categorizer(object):
    """

    Handles category management and categorization

    """
    categories = []

    def __init__(self, configs):
        self._configs = configs

    def categorize(self, window):
        """

        Categorize window according to window title
        Returns category object

        """
        for i in self.categories:
            if i.belongs(window):
                return i
        return None

    def load_categories(self):
        """

        Loads user-defined categories from application path

        """
        path = os.path.join(self._configs['appPath'])
        if os.path.exists(path):
            sys.path.append(path)
            try:
                import categories
                for name, obj in inspect.getmembers(categories):
                    if inspect.isclass(obj) and obj.__module__ == 'categories':
                        self.add_category(obj)
            except ImportError:
                print 'Category file was not loaded'

    def add_category(self, category):
        """

        Add category object to the Categorizer

        """
        if issubclass(category, Category):
            self.categories.append(category())
