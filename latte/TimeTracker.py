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
        """ Returns window time information from logs """
        log = self.get_window_stats(window)
        if log:
            return log.duration
        return None

    def get_window_stats(self, window):
        """

        Returns a dict of window statistics.
        That includes window time, category and project.

        """
        window = window.decode('unicode-escape')
        return self.session.query(Log).filter_by(window_title=window).first()

    def log(self, window):
        """ Logs window time """

        window = window.decode('unicode_escape')

        log = self.session.query(Log).filter_by(window_title=window).first()
        if log:
            log.duration += self.config.get('sleep_time')
        else:
            log = Log(window, date.today(), self.config.get('sleep_time'))
            self.session.add(log)

        self.session.commit()
