import unittest
from latte.Projects.Projectizer import Projectizer
from latte.Projects.Project import Project

class testProjectizer(unittest.TestCase):

    """

    Tests activity projectizer class

    """

    def setUp(self):
        self.configs = {
            'lattePath' : 'latte/',
        }
        self.projectizer = Projectizer(self.configs)
        self.projectizer.add_project(TestProject1)
        self.projectizer.add_project(TestProject2)

    def tearDown(self):
        pass

    def testNonExistingProject(self):

        """

        Tests if activity that does not belong to any project returns None

        """

        project = self.projectizer.projectize('Non existing project', None)
        self.assertEquals(project, None)

    def testExistingProject(self):

        """

        Tests if activity that belongs to a project returns the project

        """

        project = self.projectizer.projectize('Existing test project', None)
        self.assertEquals(isinstance(project, TestProject2), True)

class TestProject1(Project):

    def get_title(self):
        return 'TestProject1'

    def belongs(self, window, category):
        return False

class TestProject2(Project):

    def get_title(self):
        return 'TestProject2'

    def belongs(self, window, category):
        return 'test' in window
