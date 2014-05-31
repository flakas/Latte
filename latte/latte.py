#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Latte - Linux Automatic Time Tracker

Collects window titles you are working on, categorizes them and tracks time for
each window individually. Stores log data to the filesystem.

"""

import time
import subprocess
import ctypes

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from .Base import Base
from .TimeTracker import TimeTracker
from .Config import Config
from .UserActivityTracker import UserActivityTracker


class Latte(object):
    """ Main application class. """

    def __init__(self, silent=False):
        self.silent = silent
        self.config = Config()

        engine = create_engine(self.config.get('stats_db'))
        self.session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)

        self.time_tracker = TimeTracker(config=self.config, session=self.session())
        self.activity_tracker = UserActivityTracker(time_tracker=self.time_tracker, config=self.config)

    def run(self):
        if not has_required_dependencies():
            self.output("Required dependencies were not found. Please make sure `xprop` is installed and is in your PATH. Exiting...")
            return
        if not has_optional_dependencies():
            self.output("Optional dependencies were not found. Please make sure `libX11.so` and `libXss.so` are installed. Inactivity tracking will not work.")

        duration = 0
        try:
            while True:
                if self.activity_tracker.is_user_inactive():
                    self.output("User inactive")
                else:
                    title = get_active_window_title()
                    self.time_tracker.log(title)
                    stats = self.time_tracker.current_log
                    if stats:
                        self.output("%s, %s" % (title, stats.duration))
                    elif not stats:
                        self.output("IGNORED")
                time.sleep(self.config.get('sleep_time'))
        except KeyboardInterrupt:
            self.output('Exiting...')

    def get_session(self):
        return self.session()

    def output(self, text):
        if not self.silent:
            print text

def has_required_dependencies():
    """ Checks whether the system has required dependencies """
    try:
        subprocess.call(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE)
        return True
    except OSError as e:
        return False

def has_optional_dependencies():
    """ Checks whether the system has optional dependencies """
    try:
        xlib = ctypes.cdll.LoadLibrary('libX11.so')
        xss = ctypes.cdll.LoadLibrary('libXss.so')
        return True
    except OSError as e:
        return False

def get_active_window_title():
    """ Fetches active window title using xprop. """
    try:
        active = subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"],
                                  stdout=subprocess.PIPE)
        active_id = active.communicate()[0].strip().split()[-1]
        window = subprocess.Popen(["xprop", "-id", active_id, "WM_NAME"],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        result = window.communicate()[0].strip().split('"', 1)[-1][:-1]
        return unicode(result.decode('utf-8'))
    except:
        return u''


if __name__ == '__main__':
    Latte().run()
