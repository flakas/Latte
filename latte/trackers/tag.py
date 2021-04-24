import re
from latte.db import Tag

class TagTracker:
    """
    Augments a log with matching tags
    """

    def __init__(self, db):
        self.db = db
        self.load_all_tags()

    def track(self, log):
        if len(log.tags) > 0:
            # The log is already tagged, no further tags needed
            return log

        for tag in self.tags:
            if self.should_tag(log, tag):
                log.tags.append(tag)

        self.db.commit()

    def should_tag(self, log, tag):
        options = tag.get_options()
        matches = []
        if 'window_title' in options:
            matches.append(re.search(options['window_title'], log.window_title))
        if 'window_class' in options:
            matches.append(re.search(options['window_class'], log.window_class))
        if 'window_instance' in options:
            matches.append(re.search(options['window_instance'], log.window_instance))

        return len(matches) > 0 and all(matches)

    def load_all_tags(self, tags=None):
        self.tags = tags if tags else self.db.query(Tag).all()
