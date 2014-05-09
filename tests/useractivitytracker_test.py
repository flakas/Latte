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
from latte.UserActivityTracker import UserActivityTracker

class testUserActivityTracker(unittest.TestCase):
    """ A test class for the UserActivityTracker class """

    user_activity_tracker = None

    def setUp(self):
        """ Set up data used in tests """

        self.config = mock.Mock()
        def get(*args, **kwargs):
            if args[0] == 'user_inactive_threshold':
                return 10
        self.config.get = get
        self.config.getint = get

        self.time_tracker = mock.Mock()

        self.user_activity_tracker = UserActivityTracker(config=self.config, time_tracker=self.time_tracker)

    def tearDown(self):
        self.user_activity_tracker = None

    def testUserIsActiveIfIsInactiveForLessThanInactivityThreshold(self):
        """ Tests if user is not inactive if inactivity duration is less than the threshold """
        self.user_activity_tracker.get_inactivity_time = lambda: 5
        self.assertFalse(self.user_activity_tracker.is_user_inactive())

    def testInactivityDurationIsSubtractedFromCurrentLog(self):
        """ Tests that the inactivity duration is subtracted from the log duration """
        inactivity_time = 15
        self.user_activity_tracker.get_inactivity_time = lambda: inactivity_time
        self.user_activity_tracker.is_user_inactive()
        self.time_tracker.reduce_time.assert_called_with(inactivity_time)

    def testUserIsInActiveIfIsInactiveForMoreThanInactivityThreshold(self):
        """ Tests if user is inactive if inactivity duration is more than the threshold """
        self.user_activity_tracker.get_inactivity_time = lambda: 15
        self.assertTrue(self.user_activity_tracker.is_user_inactive())
