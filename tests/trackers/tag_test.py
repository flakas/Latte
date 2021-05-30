import unittest
import mock
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from latte.trackers import TagTracker

class TestTagTracker(unittest.TestCase):
    def setUp(self):
        self.db = mock.Mock()
        self.tracker = TagTracker(self.db)
        self.tag = mock.Mock(name='default tag')
        self.tag.name = 'default_tag'
        self.tag.get_options.return_value = { 'window_title': 'hello' }
        self.log = mock.Mock(window_title='hello world', window_class='test class', window_instance='some instance')
        self.log.tags = []

    def tearDown(self):
        self.tracker = None

    def test_should_tag_with_specified_matchers(self):
        self.assertTrue(self.tracker.should_tag(self.log, self.tag))
        self.tag.get_options.return_value['window_class'] = 'test'
        self.assertTrue(self.tracker.should_tag(self.log, self.tag))
        self.tag.get_options.return_value['window_instance'] = 'some'
        self.assertTrue(self.tracker.should_tag(self.log, self.tag))

    def test_should_tag_does_not_match_log(self):
        self.log.window_title = 'something else'
        self.assertFalse(self.tracker.should_tag(self.log, self.tag))

    def test_should_tag_requires_all_specified_matchers_to_match(self):
        self.tag.get_options.return_value['window_class'] = 'test'
        self.tag.get_options.return_value['window_instance'] = 'mistmatch'
        self.assertFalse(self.tracker.should_tag(self.log, self.tag))
        self.tag.get_options.return_value['window_instance'] = 'some'
        self.assertTrue(self.tracker.should_tag(self.log, self.tag))

    def test_track_does_not_add_any_tags(self):
        self.tag.get_options.return_value['window_title'] = 'should not match'
        self.tracker.load_all_tags([self.tag])
        self.tracker.track(self.log)
        self.assertTrue(len(self.log.tags) == 0)

    def test_track_adds_meta_tags(self):
        self.log.tags = [self.tag]
        meta_tag = mock.Mock(name='meta tag')
        meta_tag.get_options.return_value = { 'tag': 'default' }
        self.assertTrue(self.tracker.should_tag(self.log, meta_tag))

    def test_track_tags_log(self):
        self.tracker.load_all_tags([self.tag])
        self.tracker.track(self.log)
        self.assertTrue(len(self.log.tags) > 0)
