"""

Assignment manager class.
It loads project/category configs and handles assignment

"""
import sys
import os
import inspect

#from latte.Projects.Project import Project

class Assigner(object):
    """

    Assignment manager class.
    Handles project/category config loading and assignment

    """

    def __init__(self, assignerType, configs):
        self._configs = configs
        self._assignerType = assignerType
        self.groups = []

    def assign(self, multiple=False, *data):
        """

        Handle assigment
        Returns object if the window has been assigned

        """
        groups = []
        for i in self.groups:
            if i.belongs(*data):
                if not multiple:
                    return i
                else:
                    groups.append(i)

        if not multiple or (multiple and not groups):
            return None
        else:
            return groups

    def load_groups(self):
        """

        Loads user-defined grouping classes for project/category assignment

        """
        path = os.path.join(self._configs.get('app_path'))
        if os.path.exists(path):
            # Append system path to attempt to import config module
            sys.path.append(path)
            try:
                # Attempt to load groups
                if self._assignerType == 'project':
                    import projects as groups
                elif self._assignerType == 'category':
                    import categories as groups
            except Exception as ex:
                print '%s file was not loaded' % self._assignerType
                print repr(ex)
            # Extract and load only classes
            for name, obj in inspect.getmembers(groups):
                if inspect.isclass(obj) and obj.__module__ == groups.__name__:
                    self.add_group(obj)

    def add_group(self, group):
        """ Adds group object to groups list. """

        if self._assignerType == 'project':
            from .Projects import Project as targetClass
        elif self._assignerType == 'category':
            from .Categories import Category as targetClass

        def checkForCreatedObjects(cls, groups):
            """ Checks for registered class objects """
            for group in groups:
                if isinstance(group, cls):
                    return True
            return False

        # Make sure that it extends Category or Project Abstract Base Class
        if issubclass(group, targetClass) and \
           not checkForCreatedObjects(group, self.groups):
            self.groups.append(group())
            return True
        else:
            return False
