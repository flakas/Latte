from sqlalchemy import Column, String, Integer, Date, Unicode
from .Base import Base

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    window_title = Column(Unicode)
    date = Column(Date)
    duration = Column(Integer)

    def __init__(self, window_title, date, duration):
        self.window_title = window_title
        self.date = date
        self.duration = duration

    def __repr__(self):
        return "<Log(%s, %s, %s)>" % \
                (self.window_title, str(self.date), self.duration)

