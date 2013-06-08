import unittest
import json
import os
import shutil
import mock
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from latte.TimeTracker import TimeTracker
from latte.Config import Config
from latte.Log import Log
from latte.Base import Base

class testTimeTracker(unittest.TestCase):
    """ A test class for the TimeTracker class """

    sleepTime = 0
    timetracker = None

    def setUp(self):
        """ Set up data used in tests """

        self.config = mock.Mock()

        def get(*args, **kwargs):
            if args[0] == 'app_path':
                return 'tests/latte/'
            elif args[0] == 'sleep_time':
                return 5
            elif args[0] == 'stats_path':
                return 'stats/'
        self.config.get = get
        self.config.getint = get

        engine = create_engine('sqlite:///:memory:')
        self.session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)

        self.timetracker = TimeTracker(self.config, session=self.session())

    def tearDown(self):
        self.session().rollback()

    def testGettingEmptyLog(self):
        """ Tests if getWindowTime with empty log returns None """

        self.assertEqual(self.timetracker.get_window_time(u'Bogus'), None)

    def testAddTimeToNonExistingWindows(self):
        """ Test adding time to non existing window titles """

        window = u'Non existing window 1'
        self.timetracker.log(window)
        self.assertEqual(self.timetracker.get_window_time(window), self.config.get('sleep_time'))

    def testAddTimeToExistingWindows(self):
        window = u'Testing Window 1'
        self.timetracker.log(window)
        self.timetracker.log(window)

        self.assertEqual(self.timetracker.get_window_time(window), self.config.get('sleep_time') * 2)

    def testGetWindowStats(self):
        window = u'Some window'
        self.timetracker.log(window)

        data = self.timetracker.get_window_stats(window)
        self.assertIs(type(self.timetracker.get_window_stats(window)), Log)
