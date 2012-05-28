import unittest
from latte.Categories.Category import Category

class testCategory(unittest.TestCase):
    """

    Tests base activity category class

    """

    def testRaisesErrorWhenNotImplemented(self):
        self.assertRaises(NotImplementedError,
            Category().__getattribute__, 'title')
        self.assertRaises(NotImplementedError,
            Category().belongs, 'NotImplemented')

    def testSubclassedCategorizator(self):
        class ImplementedCategory(Category):
            title = 'Implemented Category'
            def belongs(self, window):
                return False

        c = ImplementedCategory()
        self.assertEquals(c.title, 'Implemented Category')
        self.assertEquals(c.belongs('Does not belong'), False)
