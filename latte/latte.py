#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Latte - Linux Automatic Time Tracker

Collects window titles you are working on, categorizes them and tracks time for
each window individually. Stores log data to the filesystem.

"""

import time
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from latte.db import Base
from latte.TimeTracker import TimeTracker
from latte.Config import Config
from latte.UserActivityTracker import UserActivityTracker
from latte.os.screen import Screen


class Latte(object):
    """ Main application class. """

    def __init__(self, silent=False):
        self.silent = silent
        self.config = Config()

        engine = create_engine(self.config.get('stats_db'))
        self.session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)

        self.screen = Screen()

        self.time_tracker = TimeTracker(config=self.config, session=self.session())
        self.activity_tracker = UserActivityTracker(time_tracker=self.time_tracker, config=self.config, screen=self.screen)

    def run(self):
        if not self.screen.has_required_dependencies():
            self.output("Required dependencies were not found. Please make sure `xprop` is installed and is in your PATH. Exiting...")
            return
        if not self.screen.has_optional_dependencies():
            self.output("Optional dependencies were not found. Please make sure `libX11.so` and `libXss.so` are installed. Inactivity tracking will not work.")

        try:
            self.run_tracker()
        except KeyboardInterrupt:
            self.output('Exiting...')

    def run_tracker(self):
        while True:
            if self.activity_tracker.is_user_inactive():
                self.output("User inactive")
            else:
                self.log_user_activity()
            time.sleep(self.config.get('sleep_time'))

    def log_user_activity(self):
        [title, window_class, window_instance] = self.screen.get_active_window_data()
        self.time_tracker.log(title, window_class, window_instance)
        stats = self.time_tracker.current_log
        if stats:
            self.output("[%s] %s, %s" % (window_class, title, stats.duration))
        elif not stats:
            self.output("IGNORED")

    def get_session(self):
        return self.session()

    def output(self, text):
        if not self.silent:
            print(text)

if __name__ == '__main__':
    Latte().run()
