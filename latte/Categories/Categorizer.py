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
        cats = []
        for i in self.categories:
            if i.belongs(window):
                cats.append(i)
        if cats:
            return cats
        return None

    def load_categories(self):
        """

        Loads user-defined categories from application path

        """
        # Add system path for categories if it exists
        path = os.path.join(self._configs['appPath'])
        if os.path.exists(path):
            sys.path.append(path)
            # Attempt to load categories
            try:
                import categories
                # Inspect module members and extract only classes
                for name, obj in inspect.getmembers(categories):
                    if inspect.isclass(obj) and obj.__module__ == 'categories':
                        self.add_category(obj)
            except ImportError:
                print 'Category file was not loaded'

    def add_category(self, category):
        """

        Add category object to the Categorizer

        """

        def checkForCreatedObjects(cls, categories):
            """ Checks for registered class objects """
            for cat in categories:
                if isinstance(cat, cls):
                    return True
            return False

        if issubclass(category, Category) and \
            not checkForCreatedObjects(category, self.categories):
            self.categories.append(category())
            return True
        else:
            return False
