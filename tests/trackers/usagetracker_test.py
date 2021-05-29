import unittest
import mock
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from latte.trackers import UsageTracker

class TestUsageTracker(unittest.TestCase):
    def setUp(self):
        self.db = mock.Mock()
        self.time_tracker = mock.Mock()
        self.activity_tracker = mock.Mock()
        self.tag_tracker = mock.Mock()
        self.windows = mock.Mock()

        self.tracker = UsageTracker(self.db, self.time_tracker,
                self.activity_tracker, self.tag_tracker, self.windows)
        self.active_window = mock.Mock(window_title='hello world', window_class='test class', window_instance='some instance')
        self.windows.get_active.return_value = self.active_window

    def test_track_logs_active_window(self):
        self.tracker.track()
        self.time_tracker.track.assert_called_with(self.active_window)

    def test_track_stops_tracking_if_inactive(self):
        self.activity_tracker.get_inactivity_duration.return_value = 5
        self.tracker.track()
        self.time_tracker.compensate_inactivity_and_stop_tracking.assert_called_with(5)

    def test_track_avoids_tracking_if_inactive_and_not_already_tracking(self):
        self.activity_tracker.is_inactive.return_value = True
        self.time_tracker.is_tracking.return_value = False

        self.assertTrue(self.tracker.track() is None)
