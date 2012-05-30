import sys
import os
import inspect

from Project import Project

class Projectizer:
    projects = []

    def __init__(self, configs):
        self._configs = configs

    def projectize(self, window, category):
        for i in self.projects:
            if i.belongs(window, category):
                return i
        return None

    def loadProjects(self):
        path = os.path.join(self._configs['appPath'])
        if os.path.exists(path):
            sys.path.append(path)
            try:
                import projects
                for name, obj in inspect.getmembers(projects):
                    if inspect.isclass(obj) and obj.__module__ == 'projects':
                        self.addProject(obj)
            except Exception as ex:
                print 'Cannot properly load projects'
                print ex
                pass

    def addProject(self, project):
        if issubclass(project, Project):
            self.projects.append(project())
