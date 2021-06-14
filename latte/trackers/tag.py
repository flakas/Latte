import re
from latte.db import Tag

class TagTracker:
    """
    Augments a log with matching tags
    """

    def __init__(self, db):
        self.db = db
        self.load_all_tags()
        self.regex_cache = {}

    def track(self, log):
        """ Augment the specified log with matching tags """
        if len(log.tags) > 0:
            # The log is already tagged, no further tags needed
            return log

        for tag in self.tags:
            if self.should_tag(log, tag):
                log.tags.append(tag)

    def should_tag(self, log, tag):
        options = tag.get_options()
        matches = []
        if 'window_title' in options:
            matches.append(self.find_matches(options['window_title'], log.window_title))
        if 'window_instance' in options:
            matches.append(self.find_matches(options['window_instance'], log.window_instance))
        if 'tag' in options:
            for log_tag in log.tags:
                matches.append(self.find_matches(options['tag'], log_tag.name))

        return len(matches) > 0 and all(matches)

    def find_matches(self, needle, haystack):
        if needle not in self.regex_cache:
            self.regex_cache[needle] = re.compile(needle, flags=re.IGNORECASE)
        return self.regex_cache[needle].search(haystack)

    def load_all_tags(self, tags=None):
        self.tags = tags if tags else self.db.query(Tag).all()
