from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

from latte.config import Config
from latte.db import Base

class Core:
    def __init__(self):
        self.config = Config()

        engine = create_engine(self.config.get('stats_db'))
        self.session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)

    def get_db(self):
        return self.session()
