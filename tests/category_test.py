import unittest2
from latte.Categories.Category import Category

class testCategory(unittest2.TestCase):
    """

    Tests base activity category class

    """

    def testRaisesErrorWhenNotImplemented(self):
        with self.assertRaises(NotImplementedError):
            Category().title
            Category().belongs('NotImplemented')

    def testSubclassedCategorizator(self):
        class ImplementedCategory(Category):
            title = 'Implemented Category'
            def belongs(self, window):
                return False

        c = ImplementedCategory()
        self.assertEquals(c.title, 'Implemented Category')
        self.assertEquals(c.belongs('Does not belong'), False)
