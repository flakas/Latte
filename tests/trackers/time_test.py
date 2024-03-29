import unittest
import json
import os
import shutil
import mock
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from latte.os.windows import ActiveWindow
from latte.trackers import TimeTracker
from latte.db import Base, Log

class TestTimeTracker(unittest.TestCase):
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
            elif args[0] == 'ignore_keywords':
                return ['ignore', 'keyw']
        self.config.get = get
        self.config.getint = get

        engine = create_engine('sqlite:///:memory:')
        self.session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)

        self.timetracker = TimeTracker(self.config, db=self.session())

    def tearDown(self):
        self.session().rollback()

    def test_getting_empty_log(self):
        """ Tests if getWindowTime with empty log returns None """

        self.assertEqual(self.timetracker.get_window_time(u'Bogus'), None)

    def test_add_time_to_non_existing_windows(self):
        """ Test adding time to non existing window titles """

        window = u'Non existing window 1'
        window_instance = u'New instance'
        self.timetracker.track(ActiveWindow(window, window_instance))
        self.assertEqual(self.timetracker.get_window_time(window), self.config.get('sleep_time'))

    def test_add_time_to_existing_windows(self):
        window = u'Testing Window 1'
        window_instance = u'Instance 1'
        self.timetracker.track(ActiveWindow(window, window_instance))
        self.timetracker.track(ActiveWindow(window, window_instance))

        self.assertEqual(self.timetracker.get_window_time(window), self.config.get('sleep_time') * 2)

    def test_get_window_stats(self):
        window = u'Some window'
        window_instance = u'Some instance'
        self.timetracker.track(ActiveWindow(window, window_instance))

        data = self.timetracker.get_window_stats(window)
        self.assertIs(type(self.timetracker.get_window_stats(window)), Log)

    def test_contains_ignored_keywords(self):
        window = u'Some string with ignored keywords'
        self.assertTrue(self.timetracker.contains_ignored_keywords(window))
        window2 = u'Doesn\'t contain bad words'
        self.assertFalse(self.timetracker.contains_ignored_keywords(window2))

    def test_add_log_with_ignored_keywords(self):
        window = u'Some string with ignored keywords'
        window_instance = u'Window instance'
        self.assertFalse(self.timetracker.track(ActiveWindow(window, window_instance)))
