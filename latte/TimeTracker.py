# -*- coding: utf-8 -*-
"""

Time tracking class
Handles window time logging and log information storage

"""
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from .Log import Log
import os

class TimeTracker(object):
    """ Tracks window time and stores window information. """

    def __init__(self, config, session):
        self.config = config
        self.session = session
        self.current_log = None

    def get_window_time(self, window):
        """ Return time spent on a window """
        log = self.get_window_stats(window)
        if log:
            return log.duration
        return None

    def get_window_stats(self, window):
        """ Get statistics of a window"""
        return self.session.query(Log).filter_by(window_title=window).first()

    def log(self, window):
        """ Log window time """

        if self.contains_ignored_keywords(window):
            self.current_log = None
            return False

        if self.current_log and self.current_log.window_title == window:
            self.current_log.duration += self.config.get('sleep_time')
        else:
            self.current_log = Log(window, datetime.now(), self.config.get('sleep_time'))
            self.session.add(self.current_log)

        self.session.commit()

    def contains_ignored_keywords(self, window):
        window = window.lower()
        for word in self.config.get('ignore_keywords'):
            if word in window:
                return True
        return False
