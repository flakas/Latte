import unittest

from latte.TimeTracker import TimeTracker

class testTimeTracker(unittest.TestCase):

    """

    A test class for the TimeTracker class

    """

    sleepTime = 0
    timetracker = None

    def setUp(self):

        """

        Set up data used in tests

        """

        self.sleepTime = 5
        self.timetracker = TimeTracker(self.sleepTime)
        self.timetracker.clearLogs()

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
        self.assertEqual(self.timetracker.getWindowTime(window), self.sleepTime)

    def testClearLogs(self):

        """

        Tests clearing out log data

        """

        title = 'Clearing out log data'

        self.timetracker.log(title)
        self.timetracker.clearLogs()
        self.assertEqual(self.timetracker.getWindowTime(title), None)

    def testGetAllLogs(self):

        """

        Tests fetching all data stored in logs

        """

        self.timetracker.log('Test window 1')
        self.timetracker.log('Test window 2')
        self.timetracker.log('Test window 1')
        self.assertEqual(self.timetracker.getLogs(), {
            'Test window 1' : 2 * self.sleepTime,
            'Test window 2' : self.sleepTime
        })
