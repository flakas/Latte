# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, Unicode
from .Base import Base


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    window_title = Column(Unicode)
    window_class = Column(Unicode)
    window_instance = Column(Unicode)
    date = Column(DateTime)
    duration = Column(Integer)

    def __init__(self, window_title, window_class, window_instance, date, 
                duration):
        self.window_title = window_title
        self.window_class = window_class
        self.window_instance = window_instance
        self.date = date
        self.duration = duration

    def __repr__(self):
        return "<Log(%s, %s, %s, %s, %s)>" % \
               (self.window_title, self.window_class, self.window_instance, 
                str(self.date), self.duration)

