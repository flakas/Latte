#!/usr/bin/env python

"""

Latte - Linux Automatic Time Tracker

Collects window titles you are working on, categorizes them and tracks time for
each window individually. Stores log data to the filesystem.

"""

import time
import subprocess
import os

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .Base import Base
from .TimeTracker import TimeTracker
from .Config import Config
from .Log import Log

class Latte(object):

    """ Main application class. """

    def __init__(self):
        self.config = Config()

        engine = create_engine(self.config.get('stats_db'))
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)

        self.tracker = TimeTracker(config=self.config, session=Session())

    def run(self):
        duration = 0
        try:
            while True:
                title = get_active_window_title()
                self.tracker.log(title)
                stats = self.tracker.get_window_stats(title)
                print "%s, %s" % (title, stats.duration)

                time.sleep(self.config.get('sleep_time'))
        except KeyboardInterrupt:
            print 'Exiting...'

def get_active_window_title():
    """ Fetches active window title using xprop. """
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
