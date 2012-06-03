import unittest
from latte.Projects.Project import Project

class testProject(unittest.TestCase):
    """

    Tests base activity project class

    """

    def testRaisesErrorWhenNotImplemented(self):

        """

        Test if not fully implemented category class, that inherits from Project,
        raises a NotImplementedError

        """

        self.assertRaises(NotImplementedError,
            Project().get_title)
        self.assertRaises(NotImplementedError,
            Project().belongs, 'NotImplemented', None)

    def testSubclassedProject(self):

        """

        Tests if fully implemented project class, that inherits from Project,
        does not raise a NotImplementedError

        """

        class ImplementedProject(Project):

            def get_title(self):
                return 'Implemented Project'
            def belongs(self, window):
                return False

        c = ImplementedProject()
        self.assertEquals(c.get_title(), 'Implemented Project')
        self.assertEquals(c.belongs('Does not belong'), False)
