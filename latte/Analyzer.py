# -*- coding: utf-8 -*-
"""

Latte activity log analyzer

"""

from datetime import datetime, timedelta
import errno

from sqlalchemy import *
from .Config import Config
from .Log import Log
from .latte import Latte


class Analyzer(object):
    """ Analyzes Latte log data """

    def __init__(self, config, session, args=[]):
        self.config = config
        self.since = self.parse_time_args(args)
        self.session = session

    def parse_time_args(self, args=[]):
        since = self.calculate_since('1', 'd')  # 1 day
        if len(args) == 1 and args[0] == 'all':
            since = 0
        elif len(args) == 1:
            since = self.calculate_since(args[0])
        elif len(args) == 2 and args[1] in ['d', 'w', 'm']:
            since = self.calculate_since(args[0], args[1])
        return since

    def calculate_since(self, since_str, multiplier=''):
        try:
            log_time = int(since_str, 10)
            if log_time <= 0:  # Don't allow peeking into the future
                return 0
            if multiplier:
                if multiplier == 'd':
                    log_time *= 86400  # 1 day
                elif multiplier == 'w':
                    log_time *= 604800  # 1 week
                elif multiplier == 'm':
                    log_time *= 2592000  # 1 month
            return datetime.now() - timedelta(seconds=log_time)
        except ValueError:
            print 'Cannot convert time argument to integer'
            return False

    def run(self):
        """ Main analyzer loop """
        try:
            self.analyze()
        except IOError as e:
            # Just ignore broken pipe exceptions
            if e.errno == errno.EPIPE:
                pass

    def analyze(self):
        """ Analyzes log data and prints out results """
        logs = self.session.query(Log.window_title, func.sum(Log.duration).label('duration'))
        if self.since:
            print 'Looking for log data since %s' % self.since
            logs = logs.filter(Log.date > self.since)
        logs = logs.group_by(Log.window_title).order_by('duration DESC')
        if logs.count() <= 0:
            print 'There is no log data'
            return False

        total_time = self.session.query(func.sum(Log.duration)).scalar()
        output_format = self.config.get('analyzer_output_format')

        print "Total logged time: %s\n" % self.normalize_time(total_time)
        print 'Spent time on windows:'
        for (window, duration) in logs:
            print output_format % (window.encode('utf-8'), self.normalize_time(duration))

    def normalize_time(self, seconds):
        """ Normalizes time into user-friendly form """

        if seconds <= 0:
            return '0s'

        if seconds >= 60:
            minutes = seconds / 60
            seconds %= 60
            if minutes >= 60:
                hours = minutes / 60
                minutes %= 60
                return '%dh%dm%ds' % (hours, minutes, seconds)
            else:
                return '%dm%ds' % (minutes, seconds)
        else:
            return '%ds' % seconds


if __name__ == '__main__':
    Analyzer(Config(), Latte().get_session(), sys.argv[2:]).run()
