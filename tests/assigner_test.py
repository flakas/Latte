
"""

Tests for activity category/project assignment class

"""
import unittest
from latte.Assigner import Assigner
from latte.Categories.Category import Category
from latte.Projects.Project import Project

class testCategorizer(unittest.TestCase):

    """

    Tests activity category/project assignment class

    """

    def setUp(self):
        self.configs = {
            'lattePath' : 'latte/',
        }
        self.categorizer = Assigner('category', self.configs)
        self.categorizer.add_group(TestCategory1)
        self.categorizer.add_group(TestCategory2)
        self.categorizer.add_group(TestCategory3)
        self.projectizer = Assigner('project', self.configs)

    def tearDown(self):
        self.categorizer = None
        self.projectizer = None

    def testNonExistingGroup(self):

        """

        Tests if activity that does not belong to any category returns None

        """

        category = self.categorizer.assign(True, 'Non existing category')
        self.assertEquals(category, None)

    def testCannotAddDuplicateGroups(self):

        """

        Tests if one can add duplicate groups

        """

        self.assertEqual(self.categorizer.add_group(TestCategory1), False)


    def testExistingGroup(self):

        """

        Tests if activity that belongs to a group returns the group

        """

        category = self.categorizer.assign(True, 'test')
        self.assertEquals(len(category), 1)
        self.assertEquals(isinstance(category[0], TestCategory2), True)

    def testAssignmentToMultipleCategories(self):

        """

        Tests if activity is assigned to multiple categories and that this
        returns a list of categories

        """

        categories = self.categorizer.assign(True, 'test is tested with Test3')
        self.assertEquals(len(categories), 2)
        self.assertEquals(isinstance(categories[0], TestCategory2), True)
        self.assertEquals(isinstance(categories[1], TestCategory3), True)

class TestCategory1(Category):

    def get_title(self):
        return 'TestCategory1'

    def belongs(self, window):
        return False

class TestCategory2(Category):

    def get_title(self):
        return 'TestCategory2'

    def belongs(self, window):
        return 'test' in window

class TestCategory3(Category):

    def get_title(self):
        return 'TestCategory3'

    def belongs(self, window):
        return 'test' in window and 'Test3' in window

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
