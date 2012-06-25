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

class Latte(object):

    """

    Main application class

    """

    def __init__(self, sleeptime=5, lattepath='~/.latte'):
        self.configs = {}
        self.configs['appPath'] = os.path.expanduser(lattepath)
        self.configs['statsPath'] = 'stats/'
        self.configs['sleepTime'] = sleeptime
        self.configs['autosaveTime'] = 3600
        #self.categorizer = Categorizer(configs=self.configs)
        #self.projectizer = Projectizer(configs=self.configs)
        self.categorizer = Assigner('category', self.configs)
        self.projectizer = Assigner('project', self.configs)
        self.tracker = TimeTracker(configs=self.configs,
                                   categorizer=self.categorizer,
                                   projectizer=self.projectizer)

        # Register a cleanup
        atexit.register(self.cleanup)

        # Add application configuration path
        if not os.path.exists(self.configs['appPath']):
            os.makedirs(self.configs['appPath'])

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

            time.sleep(self.configs['sleepTime'])
            # Track time since last save and do autosaves
            duration += self.configs['sleepTime']
            if duration >= self.configs['autosaveTime']:
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
    Latte(sleeptime=5, lattepath='~/.latte').run()
