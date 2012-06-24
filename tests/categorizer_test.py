"""

Tests for activity categorization class

"""
import unittest
from latte.Categories.Categorizer import Categorizer
from latte.Categories.Category import Category

class testCategorizer(unittest.TestCase):

    """

    Tests activity categorization class

    """

    def setUp(self):
        self.configs = {
            'lattePath' : 'latte/',
        }
        self.categorizer = Categorizer(self.configs)
        self.categorizer.add_category(TestCategory1)
        self.categorizer.add_category(TestCategory2)
        self.categorizer.add_category(TestCategory3)

    def tearDown(self):
        self.categorizer = None

    def testNonExistingCategory(self):

        """

        Tests if activity that does not belong to any category returns None

        """

        category = self.categorizer.categorize('Non existing category')
        self.assertEquals(category, None)

    def testCannotAddDuplicateCategories(self):

        """

        Tests if one can add duplicate categories

        """
        
        self.assertEqual(self.categorizer.add_category(TestCategory1), False)


    def testExistingCategory(self):

        """

        Tests if activity that belongs to a category returns the category

        """

        category = self.categorizer.categorize('test')
        print category
        print self.categorizer.categories
        self.assertEquals(len(category), 1)
        self.assertEquals(isinstance(category[0], TestCategory2), True)

    def testAssignmentToMultipleCategories(self):

        """

        Tests if activity is assigned to multiple categories and that this
        returns a list of categories

        """

        categories = self.categorizer.categorize('test is tested with Test3')
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
