"""

Project management class.
It loads project configs and handles project assignment

"""
import sys
import os
import inspect

from Project import Project

class Projectizer(object):
    """

    Project management class.
    Handles project config loading and project assignment

    """
    projects = []

    def __init__(self, configs):
        self._configs = configs

    def projectize(self, window, category):
        """

        Assign window to a project.
        Returns Project object if the window has been assigned

        """
        for i in self.projects:
            if i.belongs(window, category):
                return i
        return None

    def load_projects(self):
        """

        Loads user-defined project classes for project assignment

        """
        path = os.path.join(self._configs['appPath'])
        if os.path.exists(path):
            sys.path.append(path)
            try:
                import projects
                for name, obj in inspect.getmembers(projects):
                    if inspect.isclass(obj) and obj.__module__ == 'projects':
                        self.add_project(obj)
            except Exception as ex:
                print 'Cannot properly load projects'
                print ex

    def add_project(self, project):
        """

        Adds project object to projects list

        """
        if issubclass(project, Project):
            self.projects.append(project())
