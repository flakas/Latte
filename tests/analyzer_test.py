import unittest
from unittest.mock import MagicMock
import os
from latte.analyzer.Analyzer import Analyzer

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.config = {}
        self.config['appPath'] = os.path.expanduser('latte/')
        self.config['statsPath'] = 'stats/'
        self.config['sleepTime'] = 5
        self.config['autosaveTime'] = 3600

        self.arguments = MagicMock()

        self.analyzer = Analyzer(self.config, {}, self.arguments)

    def tearDown(self):
        pass

    def testGetHumanReadableDuration(self):
        """ Tests pretty time formatting """
        self.assertEqual(self.analyzer.get_human_readable_duration(0), '0s')
        self.assertEqual(self.analyzer.get_human_readable_duration(-1), '0s')
        self.assertEqual(self.analyzer.get_human_readable_duration(10), '10s')
        self.assertEqual(self.analyzer.get_human_readable_duration(60), '1m')
        self.assertEqual(self.analyzer.get_human_readable_duration(119), '1m59s')
        self.assertEqual(self.analyzer.get_human_readable_duration(3600), '1h')
        self.assertEqual(self.analyzer.get_human_readable_duration(3661), '1h1m1s')
