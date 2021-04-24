# -*- coding: utf-8 -*-
import json
from sqlalchemy import Column, Integer, DateTime, Unicode
from . import Base


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    options = Column(Unicode)

    def __init__(self, name, options):
        self.name = name
        self.options = options

    def __repr__(self):
        return "<Tag(%s, %s)>" % (self.name, self.options)

    def get_options(self):
        return json.loads(self.options)

    def set_options(self, options):
        self.options = json.dumps(options)
