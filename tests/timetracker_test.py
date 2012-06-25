import unittest
import json
import os
import shutil

from latte.TimeTracker import TimeTracker
from latte.Assigner import Assigner

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

        self.configs = {
            'sleepTime' : 5,
            'appPath' : 'tests/latte/',
            'statsPath' : 'stats/',
        }
        self.categorizer = Assigner('category', self.configs)
        self.projectizer = Assigner('project', self.configs)
        self.timetracker = TimeTracker(self.configs, self.categorizer, self.projectizer)
        self.timetracker.clear_logs()

    def tearDown(self):
        try:
            shutil.rmtree(self.configs['appPath'])
        except Exception as ex:
            pass

    def testSleepTimeIsSet(self):

        """

        Tests if sleepTime is being set properly

        """

        self.assertEqual(self.timetracker.get_sleep_time(), self.configs['sleepTime'])

    def testGettingEmptyLog(self):

        """

        Tests if getWindowTime with empty log returns None

        """

        self.assertEqual(self.timetracker.get_window_time('Bogus'), None)

    def testAddTimeToNonExistingWindows(self):

        """

        Test adding time to non existing window titles

        """

        window = 'Non existing window 1'
        self.timetracker.log(window)
        self.assertEqual(self.timetracker.get_window_time(window), self.configs['sleepTime'])

    def testClearLogs(self):

        """

        Tests clearing out log data

        """

        title = 'Clearing out log data'

        self.timetracker.log(title)
        self.timetracker.clear_logs()
        self.assertEqual(self.timetracker.get_window_time(title), None)

    def testGetAllLogs(self):

        """

        Tests fetching all data stored in logs

        """

        self.timetracker.log('Test window 1')
        self.timetracker.log('Test window 2')
        self.timetracker.log('Test window 1')
        self.assertEqual(self.timetracker.get_logs(), {
            'Test window 1' : {
                'time' : 2 * self.configs['sleepTime'],
                'categories' : [],
                'project' : '',
            },
            'Test window 2' : {
                'time' : self.configs['sleepTime'],
                'categories' : [],
                'project' : '',
            }
        })

    def testDumpLogToFile(self):

        """

        Tests dumping log data to file

        """

        self.timetracker.clear_logs()
        self.timetracker.log('Dump Log To File')
        str = json.dumps(self.timetracker.get_logs(), indent=4)
        filename = self.timetracker.dump_logs()
        file_path = os.path.join(
            self.configs['appPath'],
            self.configs['statsPath'],
            filename
        )
        self.assertTrue(os.path.exists(file_path))

        file = open(file_path, 'r')
        contents = file.read()
        file.close()

        self.assertEqual(str, contents)
