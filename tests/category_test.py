import unittest
from latte.Categories.Category import Category

class testCategory(unittest.TestCase):
    """

    Tests base activity category class

    """

    def testRaisesErrorWhenNotImplemented(self):

        """

        Test if not fully implemented category class, that inherits from Category,
        raises a NotImplementedError

        """

        self.assertRaises(NotImplementedError,
            Category().getTitle)
        self.assertRaises(NotImplementedError,
            Category().belongs, 'NotImplemented')

    def testSubclassedCategorizator(self):

        """

        Tests if fully implemented category class, that inherits from Category,
        does not raise a NotImplementedError

        """

        class ImplementedCategory(Category):
            title = 'Implemented Category'
            def belongs(self, window):
                return False

        c = ImplementedCategory()
        self.assertEquals(c.title, 'Implemented Category')
        self.assertEquals(c.belongs('Does not belong'), False)
