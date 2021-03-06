# -*- coding: utf-8 -*-
"""

Latte activity log analyzer

"""

from datetime import datetime, timedelta
import errno
import math

from sqlalchemy import *
from latte.analyzer.arguments import Arguments
from latte.Config import Config
from latte.Log import Log
from latte.latte import Latte


class Analyzer(object):
    """ Analyzes Latte log data """

    def __init__(self, config, db, arguments):
        self.config = config
        self.db = db
        self.arguments = arguments

        self.parse_args()

    def parse_args(self):
        """Parses command line arguments"""

        self.arguments.parse()

        self.since = self.parse_time_args()
        self.group = self.arguments.get('g')
        self.order = self.arguments.get('o')

    def parse_time_args(self):
        default_since = self.calculate_since(1, 86400)  # 1 day

        if self.arguments.get('time_all'):
            return 0

        options = [
            ('time_seconds', 1),
            ('time_days', 86400),
            ('time_weeks', 604800),
            ('time_months', 2592000)
        ]

        for (key, multiplier) in options:
            duration = self.arguments.get(key)
            if self.arguments.get(key):
                return self.calculate_since(duration, multiplier)

        return default_since

    def calculate_since(self, log_time, multiplier=1):
        if log_time <= 0:  # Don't allow peeking into the future
            return 0

        log_time *= multiplier

        return datetime.now() - timedelta(seconds=log_time)

    def run(self):
        """ Main analyzer loop """
        try:
            self.analyze()
        except IOError as e:
            # Just ignore broken pipe exceptions
            if e.errno == errno.EPIPE:
                pass

    def analyzer_output(self, logs):
        total_time = self.get_total_time()
        print("Total logged time: %s\n" % self.get_human_readable_duration(total_time))
        print('Spent time on windows:')
        if self.group == 'class':
            output_format = self.config.get('analyzer_output_class')
            for row in logs:
                duration = self.get_human_readable_duration(row[1])
                window_class = self.get_alias(row[2])
                print(output_format % (window_class, duration))
        elif self.group == 'instance':
            output_format = self.config.get('analyzer_output_instance')
            for row in logs:
                duration = self.get_human_readable_duration(row[1])
                window_instance = row[3]
                print(output_format % (window_instance, duration))
        else:
            output_format = self.config.get('analyzer_output_default')
            for row in logs:
                window = row[0]
                duration = self.get_human_readable_duration(row[1])
                window_class = self.get_alias(row[2])
                window_instance = row[3]
                print(output_format % (window_class, window_instance, window, duration))

    def get_alias(self, raw):
        alias = ''
        alias_config = self.config.get('aliases')
        if (alias_config != None and alias_config.has_key(raw)) == True:
            alias =  self.config.get('aliases')[raw]
        else:
            alias = raw
        return alias

    def get_total_time(self):
        return self.db.query(func.sum(Log.duration)).scalar()

    def analyze(self):
        """ Analyzes log data and prints out results """
        logs = self.db.query(
            Log.window_title,
            func.sum(Log.duration).label('duration'),
            Log.window_class,
            Log.window_instance
        )

        if self.since:
            print('Looking for log data since %s' % self.since)
            logs = logs.filter(Log.date > self.since)

        logs = self.set_grouping(logs)
        logs = self.set_ordering(logs)
        logs = self.set_result_limiting(logs)

        if logs.count() <= 0:
            print('There is no log data')
            return False

        self.analyzer_output(logs)

    def set_grouping(self, query):
        groups = {
            'title': 'window_title',
            'instance': 'window_instance',
            'class': 'window_class'
        }

        return query.group_by(getattr(Log, groups[self.group]))

    def set_ordering(self, query):
        ordering = asc('duration') if self.order == 'asc' else desc('duration')
        return query.order_by(ordering)

    def set_result_limiting(self, query):
        if self.arguments.get('display_all'):
            return query

        limit = self.arguments.get('display_limit')
        if limit:
            return query.limit(limit)

        share = self.arguments.get('display_share')
        if share:
            percentage = 1 / (100.0 / share)
            threshold = self.get_total_time() * percentage
            return query.having(func.sum(Log.duration) >= threshold)

        min_time = self.arguments.get('display_time')
        if min_time:
            return query.having(func.sum(Log.duration) >= min_time)

        return query

    def get_human_readable_duration(self, total_seconds):
        """ Normalizes time into user-friendly form """

        if total_seconds <= 0:
            return '0s'

        hours = math.floor(total_seconds / 3600)
        minutes = math.floor((total_seconds % 3600) / 60)
        seconds = total_seconds % 60

        intervals = [(hours, '%dh'), (minutes, '%dm'), (seconds, '%ds')]

        nonzero_intervals = filter(lambda i: i[0] > 0, intervals)
        formatted_intervals = map(lambda i: i[1] % i[0], nonzero_intervals)

        return ''.join(formatted_intervals)

if __name__ == '__main__':
    Analyzer(Config(), Latte().get_session(), Arguments(sys.argv)).run()
