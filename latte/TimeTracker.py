"""

Time tracking class
Handles window time logging and log information storage

"""
from sqlalchemy.orm.exc import NoResultFound
from datetime import date
from .Log import Log
import os

class TimeTracker(object):
    """ Tracks window time and stores window information. """

    def __init__(self, config, session):
        self.config = config
        self.session = session

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
            return False

        log = self.session.query(Log).filter_by(window_title=window).first()
        if log:
            log.duration += self.config.get('sleep_time')
        else:
            log = Log(window, date.today(), self.config.get('sleep_time'))
            self.session.add(log)

        self.session.commit()

    def contains_ignored_keywords(self, window):
        window = window.lower()
        for word in self.config.get('ignore_keywords'):
            if word in window:
                return True
        return False
