#!/usr/bin/env python

"""

Latte - Linux Automatic Time Tracker

Collects window titles you are working on, categorizes them and tracks time for
each window individually. Stores log data to the filesystem.

"""

import time
import subprocess
import os
import atexit

from .TimeTracker import TimeTracker
from .Assigner import Assigner
from .Config import Config

class Latte(object):

    """

    Main application class

    """

    def __init__(self):
        self.configs = Config()
        self.categorizer = Assigner('category', self.configs)
        self.projectizer = Assigner('project', self.configs)
        self.tracker = TimeTracker(configs=self.configs,
                                   categorizer=self.categorizer,
                                   projectizer=self.projectizer)

        # Register a cleanup
        atexit.register(self.cleanup)

        # Add application configuration path
        if not os.path.exists(self.configs.get('app_path')):
            os.makedirs(self.configs.get('app_path'))

    def cleanup(self):
        """

        Atexit cleanup method. Force dumps log information to the filesystem

        """
        self.tracker.dump_logs()

    def run(self):
        """

        Primary application loop

        """
        duration = 0
        while True:
            title = get_active_window_title()
            if title:
                self.tracker.log(title)
                stats = self.tracker.get_window_stats(title)
                print title, \
                    repr(stats['categories']), \
                    repr(stats['project']), \
                    stats['time']

            time.sleep(self.configs.getint('sleep_time'))
            # Track time since last save and do autosaves
            duration += self.configs.getint('sleep_time')
            if duration >= self.configs.getint('autosave_time'):
                duration = 0
                self.tracker.dump_logs()

def get_active_window_title():
    """

    Fetches active window title using xprop

    """
    try:
        active = subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"],
                                stdout=subprocess.PIPE)
        active_id = active.communicate()[0].strip().split()[-1]
        window = subprocess.Popen(["xprop", "-id", active_id, "WM_NAME"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        return window.communicate()[0].strip().split('"', 1)[-1][:-1]
    except:
        return ''


if __name__ == '__main__':
    Latte().run()
