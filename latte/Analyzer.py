"""

Latte activity log analyzer

"""

import os
import json
import time

from .Config import Config

class Analyzer(object):
    """ Analyzes Latte log data """

    def __init__(self, config, args=[]):
        self.config = config
        self.logs = {}
        self.since = 0
        if len(args) == 1:
            try:
                log_time = int(args[0], 10)
                if log_time > 0:
                    self.since = time.time() - log_time
            except:
                print 'Cannot convert time argument to integer'
        elif len(args) == 2 and args[1] in ['d', 'w', 'm']:
            try:
                log_time = int(args[0], 10)
                if log_time > 0:
                    converted = True
            except:
                print 'Cannot convert time argument to integer'
            if converted:
                if args[1] == 'd':
                    log_time *= 86400 #1 day
                elif args[1] == 'w':
                    log_time *= 604800 #1 week
                elif args[1] == 'm':
                    log_time *= 2592000 #1 month
                self.since = time.time() - log_time

    def run(self):
        """ Main analyzer loop """
        self.load_logs()
        #print repr(self.logs)
        self.analyze()

    def analyze(self):
        """ Analyzes log data and prints out results """
        if self.since:
            print 'Looking for log data since %s' % time.strftime('%d %b %Y %H:%M:%S', time.gmtime(self.since))
        if not self.logs:
            print 'There is no log data'
            return False

        windows = {}
        categories = {}
        projects = {}
        totalLogs = 0
        totalTime = 0

        # Log files
        for logFileKey in self.logs.keys():
            logFile = self.logs[logFileKey]
            totalLogs += len(logFile)
            # Individual log entries
            for logKey in logFile.keys():
                log = logFile[logKey]
                totalTime += log['time']
                if not windows.has_key(logKey):
                    windows[logKey] = log['time']
                else:
                    windows[logKey] += log['time']
                if not projects.has_key(log['project']):
                    projects[log['project']] = log['time']
                else:
                    projects[log['project']] += log['time']
                if 'categories' in log.keys():
                    if not log['categories']:
                        log['categories'] = ['(Uncategorized)']
                    # Assign time to individual categories
                    for cat in log['categories']:
                        if not categories.has_key(cat):
                            categories[cat] = log['time']
                        else:
                            categories[cat] += log['time']

        print 'Total log files: %d\nTotal log entries: %d' % (len(self.logs), \
                                                              totalLogs)
        print 'Total logged time: %s' % self.normalize_time(totalTime)
        print ''
        print 'Spent time on windows:'
        sortedWindowTimes = sorted(windows.items(), \
                                   cmp=lambda x, y: cmp(x[1], y[1]), \
                                   reverse=True)
        for (window, spent) in sortedWindowTimes:
            print '- "%s" : %s' % (window, self.normalize_time(spent))

        print ''
        print 'Spent time on categories:'
        for (category, spent) in categories.items():
            print '- "%s" : %s' % (category, self.normalize_time(spent))

        print ''
        print 'Spent time on projects:'
        for (project, spent) in projects.items():
            print '- "%s" : %s' % (project, self.normalize_time(spent))


    def load_logs(self):
        """ Loads logs from log files and stores them in memory """

        # Get a list of log files available
        logsPath = os.path.join(self.config.get('app_path'), \
                                self.config.get('stats_path'))
        logFiles = os.listdir(logsPath)
        if not logFiles:
            return False

        if self.since:
            since = str(self.since)
            logFiles = filter(lambda x: x >= since, logFiles)


        # Attempt to open each file, read and parse log data
        for logFile in logFiles:
            path = os.path.join(logsPath, logFile)
            logFileHandle = open(path, 'r')
            contents = logFileHandle.read()
            # File data may be corrupted
            try:
                jsonContents = json.loads(contents)
                self.logs[logFile] = jsonContents
            except ValueError:
                continue
            logFileHandle.close()
        return True

    def normalize_time(self, seconds):
        """ Normalizes time into user-friendly form """

        if seconds <= 0:
            return '0s'

        if seconds >= 60:
            minutes = seconds / 60
            seconds = seconds % 60
            if minutes >= 60:
                hours = minutes / 60
                minutes = minutes % 60
                return '%dh%dm%ds' % (hours, minutes, seconds)
            else:
                return '%dm%ds' % (minutes, seconds)
        else:
            return '%ds' % seconds

if __name__ == '__main__':
    Analyzer(Config()).run()
