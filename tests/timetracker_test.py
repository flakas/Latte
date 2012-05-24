import unittest

from latte.TimeTracker import TimeTracker

class testTimeTracker(unittest.TestCase):

    """

    A test class for the TimeTracker class

    """

    def setUp(self):

        """

        Set up data used in tests

        """

        self.sleepTime = 5
        self.timetracker = TimeTracker(self.sleepTime)

    def testSleepTimeIsSet(self):

        """

        Tests if sleepTime is being set properly

        """

        self.assertEqual(self.timetracker.getSleepTime(), self.sleepTime)

    def testGettingEmptyLog(self):

        """

        Tests if getWindowTime with empty log returns None

        """

        self.assertEqual(self.timetracker.getWindowTime('Bogus'), None)

    def testAddTimeToNonExistingWindows(self):
        """

        Test adding time to non existing window titles

        """

        window = 'Non existing window 1'
        self.timetracker.log(window)
        self.assertEqual(self.timetracker.getWindowTime(window), self.timetracker.getSleepTime())
