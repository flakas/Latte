"""

Project management class.
It loads project configs and handles project assignment

"""
import sys
import os
import inspect

from latte.Projects.Project import Project

class Projectizer(object):
    """

    Project management class.
    Handles project config loading and project assignment

    """
    projects = []

    def __init__(self, configs):
        self._configs = configs

    def projectize(self, window, categories):
        """

        Assign window to a project.
        Returns Project object if the window has been assigned

        """
        for i in self.projects:
            if i.belongs(window, categories):
                return i
        return None

    def load_projects(self):
        """

        Loads user-defined project classes for project assignment

        """
        path = os.path.join(self._configs['appPath'])
        if os.path.exists(path):
            # Append system path to attempt to import config module
            sys.path.append(path)
            try:
                # Attempt to load projects
                import projects
                # Extract and load only classes
                for name, obj in inspect.getmembers(projects):
                    if inspect.isclass(obj) and obj.__module__ == 'projects':
                        self.add_project(obj)
            except Exception as ex:
                print 'Project file was not loaded'
                print repr(ex)

    def add_project(self, project):
        """

        Adds project object to projects list

        """
        # Make sure that it extends Project Abstract Base Class
        if issubclass(project, Project):
            self.projects.append(project())
