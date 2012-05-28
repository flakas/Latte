import unittest
from latte.Categories.Categorizer import Categorizer
from latte.Categories.Category import Category

class testCategorizer(unittest.TestCase):

    """

    Tests activity categorization class

    """

    def setUp(self):
        self.categories = (TestCategory1(), TestCategory2())
        self.categorizer = Categorizer(self.categories)

    def tearDown(self):
        pass

    def testNonExistingCategory(self):

        """

        Tests if activity that does not belong to any category returns None

        """

        category = self.categorizer.categorize('Non existing category')
        self.assertEquals(category, None)

    def testExistingCategory(self):

        """

        Tests if activity that belongs to a category returns the category

        """

        category = self.categorizer.categorize('Existing test category')
        self.assertEquals(isinstance(category, TestCategory2), True)

class TestCategory1(Category):

    def getTitle(self):
        return 'TestCategory1'

    def belongs(self, window):
        return False

class TestCategory2(Category):

    def getTitle(self):
        return 'TestCategory2'

    def belongs(self, window):
        return 'test' in window
