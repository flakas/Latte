# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, Unicode, Table, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

LogTags = Table('log_tags', Base.metadata,
    Column('log_id', Integer, ForeignKey('logs.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    window_title = Column(Unicode)
    window_class = Column(Unicode)
    window_instance = Column(Unicode)
    date = Column(DateTime)
    duration = Column(Integer)
    tags = relationship("Tag", secondary=LogTags, back_populates='logs')

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
