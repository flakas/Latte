"""

Time tracking class
Handles window time logging and log information storage

"""
import time
import json
import os

class TimeTracker(object):
    """

    Tracks window time and stores window information

    """

    logs = {}

    def __init__(self, configs, categorizer, projectizer):
        self._configs = configs
        self._categorizer = categorizer
        self._projectizer = projectizer
        # Load category and project configs
        self._categorizer.load_groups()
        self._projectizer.load_groups()

    def get_window_time(self, window):
        """

        Returns window time information from logs

        """
        if window in self.logs.keys():
            return self.logs[window]['time']
        else:
            return None

    def get_window_stats(self, window):
        """

        Returns a dict of window statistics.
        That includes window time, category and project.

        """
        if window in self.logs.keys():
            return self.logs[window]
        else:
            return None

    def log(self, window):
        """

        Logs window time, handles assigning to projects and categories.

        """
        if not window in self.logs.keys():
            self.logs[window] = {
                'time' : 0,
                'categories' : [],
                'project' : ''
            }
            categories = self._categorizer.assign(True, window)
            if categories:
                self.logs[window]['categories'] = [c.get_title() for c in categories]
            project = self._projectizer.assign(False, window, categories)
            if project:
                self.logs[window]['project'] = project.get_title()
        self.logs[window]['time'] += self._configs.get('sleep_time')

    def get_logs(self):
        """

        Returns whole logs dict

        """

        return self.logs

    def clear_logs(self):
        """

        Removes logs, stored in this object

        """
        self.logs = {}

    def dump_logs(self):
        """

        Dumps logs to filesystem

        """
        # Join stats system path and create it if it doesn't exist
        target_path = os.path.join(self._configs.get('app_path'),
                                   self._configs.get('stats_path'))
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        # Filename for current timestamp
        filename = str(int(time.time()))
        file_path = os.path.join(target_path, filename)

        # Write logs in json format to the log file
        log_file = open(file_path, 'w')
        log_file.write(json.dumps(self.get_logs(), indent=4))
        log_file.close()

        self.clear_logs()
        return filename
