import unittest
import json
import os
import shutil
import mock
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from latte.trackers import UserActivityTracker

class TestUserActivityTracker(unittest.TestCase):
    """ A test class for the UserActivityTracker class """

    user_activity_tracker = None

    def setUp(self):
        """ Set up data used in tests """

        self.idle_detector = mock.Mock()
        self.idle_detector.is_available.return_value = True

        self.inactivity_threshold = 60

        self.tracker = UserActivityTracker(self.idle_detector, self.inactivity_threshold)

    def tearDown(self):
        self.tracker = None

    def testUserIsActiveIfIsInactiveForLessThanInactivityThreshold(self):
        """ Tests that user is active if inactivity duration is less than the threshold """
        self.idle_detector.get_idle_time.return_value = self.inactivity_threshold - 1
        self.assertFalse(self.tracker.is_inactive())

    def testUserIsInActiveIfIsInactiveForMoreThanInactivityThreshold(self):
        """ Tests if user is inactive if inactivity duration is more than the threshold """
        self.idle_detector.get_idle_time.return_value = self.inactivity_threshold + 1
        self.assertTrue(self.tracker.is_inactive())
