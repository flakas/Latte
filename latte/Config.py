"""

Config class

Handles application configuration loading

"""

import ConfigParser
import os

class Config(object):
    """ Handles config loading and parsing. """

    def __init__(self, path='~/.latte'):
        self.config = ConfigParser.ConfigParser()
        self.load_config(path)
        self.config.set('main', 'app_path', os.path.expanduser(path))

    def load_config(self, path):
        """ Attempt to load configs from default path. """
        self.config.read(os.path.expanduser(path + '/config'))

    def get(self, item, section='main'):
        """ Fetches config item from the list. """
        return self.config.get(section, item)

    def getint(self, item, section='main'):
        """ Attempts to fetch config item as integer. """
        return self.config.getint(section, item)


if __name__ == '__main__':
    Config()
