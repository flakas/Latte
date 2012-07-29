import unittest
import json
import os
import shutil
import mock

from latte.TimeTracker import TimeTracker
from latte.Assigner import Assigner
from latte.Config import Config

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

        self.configs = mock.Mock()

        def get(*args, **kwargs):
            if args[0] == 'app_path':
                return 'tests/latte/'
            elif args[0] == 'sleep_time':
                return 5
            elif args[0] == 'stats_path':
                return 'stats/'
        self.configs.get = get
        self.configs.getint = get

        self.categorizer = Assigner('category', self.configs)
        self.projectizer = Assigner('project', self.configs)
        self.timetracker = TimeTracker(self.configs, self.categorizer, self.projectizer)
        self.timetracker.clear_logs()

    def tearDown(self):
        try:
            shutil.rmtree(self.configs.get('app_path'))
        except Exception as ex:
            pass

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
        self.assertEqual(self.timetracker.get_window_time(window), self.configs.get('sleep_time'))

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
                'time' : 2 * self.configs.get('sleep_time'),
                'categories' : [],
                'project' : '',
            },
            'Test window 2' : {
                'time' : self.configs.get('sleep_time'),
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
            self.configs.get('app_path'),
            self.configs.get('stats_path'),
            filename
        )
        self.assertTrue(os.path.exists(file_path))

        file = open(file_path, 'r')
        contents = file.read()
        file.close()

        self.assertEqual(str, contents)
