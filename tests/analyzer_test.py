import unittest
import os
from latte.Analyzer import Analyzer

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.config = {}
        self.config['appPath'] = os.path.expanduser('latte/')
        self.config['statsPath'] = 'stats/'
        self.config['sleepTime'] = 5
        self.config['autosaveTime'] = 3600

        self.analyzer = Analyzer(self.config, {})

    def tearDown(self):
        pass

    def testNormalizeTime(self):
        """ Tests time normalization """
        self.assertEqual(self.analyzer.normalize_time(0), '0s')
        self.assertEqual(self.analyzer.normalize_time(-1), '0s')
        self.assertEqual(self.analyzer.normalize_time(10), '10s')
        self.assertEqual(self.analyzer.normalize_time(60), '1m')
        self.assertEqual(self.analyzer.normalize_time(119), '1m59s')
        self.assertEqual(self.analyzer.normalize_time(3600), '1h')
        self.assertEqual(self.analyzer.normalize_time(3661), '1h1m1s')
