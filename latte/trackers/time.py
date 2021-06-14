# -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, date
from latte.db import Log


class TimeTracker(object):
    """ Tracks window time and stores window information. """

    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.current_log = None

    def is_tracking(self):
        return self.current_log != None

    def track(self, active_window):
        """ Log window time """

        if self.contains_ignored_keywords(active_window.title):
            return self.stop_tracking()

        if (self.current_log and self.current_log.window_title == active_window.title and
                self.current_log.date.date() == date.today()):
            self.current_log.duration += self.config.get('sleep_time')
        else:
            self.current_log = Log(
                    active_window.title,
                    active_window.instance, datetime.now(),
                    self.config.get('sleep_time'))
            self.db.add(self.current_log)

        self.db.commit()
        return self.current_log

    def stop_tracking(self):
        self.current_log = None
        return False

    def compensate_inactivity_and_stop_tracking(self, inactivity_duration):
        '''
        Compensates time spent on a window if inactivity is confirmed
        and stops tracking
        '''
        if self.current_log:
            self.current_log.duration = min(self.current_log.duration - inactivity_duration, 0)
            self.db.commit()
            self.stop_tracking()
            return True
        else:
            return False

    def get_window_time(self, window_title):
        """ Return time spent on a window """
        log = self.get_window_stats(window_title)
        if log:
            return log.duration
        return None

    def get_window_stats(self, window_title):
        """ Get statistics of a window"""
        return self.db.query(Log).filter_by(window_title=window_title).first()

    def contains_ignored_keywords(self, window_title):
        window_title = window_title.lower()
        for word in self.config.get('ignore_keywords'):
            if word in window_title:
                return True
        return False
