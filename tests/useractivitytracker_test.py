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
        self.screen = mock.Mock()
        self.screen.is_available.return_value = True

        self.user_activity_tracker = UserActivityTracker(config=self.config, time_tracker=self.time_tracker, screen=self.screen)

    def tearDown(self):
        self.user_activity_tracker = None

    def testUserIsActiveIfIsInactiveForLessThanInactivityThreshold(self):
        """ Tests that user is active if inactivity duration is less than the threshold """
        self.screen.get_idle_time.return_value = 5
        self.assertFalse(self.user_activity_tracker.is_user_inactive())

    def testInactivityDurationIsSubtractedFromCurrentLog(self):
        """ Tests that the inactivity duration is subtracted from the log duration """
        inactivity_time = 15
        self.screen.get_idle_time.return_value = 15
        self.user_activity_tracker.is_user_inactive()
        self.time_tracker.reduce_time.assert_called_with(inactivity_time)

    def testUserIsInActiveIfIsInactiveForMoreThanInactivityThreshold(self):
        """ Tests if user is inactive if inactivity duration is more than the threshold """
        self.screen.get_idle_time.return_value = 15
        self.assertTrue(self.user_activity_tracker.is_user_inactive())
