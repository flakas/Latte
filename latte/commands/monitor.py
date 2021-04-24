#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from latte.trackers import TimeTracker, UsageTracker, UserActivityTracker, TagTracker
from latte.os import Windows, IdleDetector


class Monitor(object):
    """ Collects data on computer usage """

    def __init__(self, config, db, silent=False):
        self.config = config
        self.db = db
        self.silent = silent

        self.windows = Windows()
        self.idle_detector = IdleDetector()

        self.time_tracker = TimeTracker(config=self.config, db=self.db)
        self.activity_tracker = UserActivityTracker(
                idle_detector=self.idle_detector,
                inactivity_threshold=self.config.get('user_inactive_threshold'))
        self.usage_tracker = UsageTracker(self.time_tracker, self.activity_tracker, self.windows)
        self.tag_tracker = TagTracker(db=self.db)

    def run(self):
        if not self.windows.has_required_dependencies():
            self.output("Required dependencies were not found. Please make sure `xprop` is installed and is in your PATH. Exiting...")
            return
        if not self.idle_detector.has_optional_dependencies():
            self.output("Optional dependencies were not found. Please make sure `libX11.so` and `libXss.so` are installed. Inactivity tracking will not work.")

        try:
            self.run_tracker()
        except KeyboardInterrupt:
            self.output('Exiting...')

    def run_tracker(self):
        while True:
            self.show_tracking_result(self.usage_tracker.track())
            time.sleep(self.config.get('sleep_time'))

    def show_tracking_result(self, log):
        if log:
            self.output("[%s] %s, %s" % (log.window_class, log.window_title, log.duration))
        else:
            self.output("IGNORED")

    def output(self, text):
        if not self.silent:
            print(text)
