# -*- coding: utf-8 -*-
"""

Config class

Handles application configuration loading

"""

import ConfigParser
import os


class Config(object):
    """ Handles config loading and parsing. """

    def __init__(self, path='~/.config/latte'):
        self.config = {}
        self.user_config_path = os.path.expanduser(path)

        self.load_default_configs()
        self.create_default_configs()
        self.load_user_config(path)

    def load_default_configs(self):
        """ Load default config values. """
        self.set('app_path', self.user_config_path)
        self.set('stats_db', 'sqlite:////%s/stats.db' % self.user_config_path)
        self.set('sleep_time', 5)
        self.set('ignore_keywords', [])
        self.set('user_inactive_threshold', 30)

    def set(self, name, value):
        """ Set config value. """
        self.config[name] = value

    def create_default_configs(self):
        # Create main application folder
        if not os.path.exists(self.config.get('app_path')):
            os.makedirs(self.config.get('app_path'))

    def load_user_config(self, path):
        """ Attempt to load configs from default path. """
        path = os.path.expanduser(path + '/config')
        if os.path.exists(path):
            parser = ConfigParser.ConfigParser()
            parser.read(path)
            self.overwrite_with_user_configs(parser)
            return True
        else:
            return False

    def overwrite_with_user_configs(self, parser):
        """ Overwrite default configs with user-defined configs. """
        for item in ['stats_db']:
            self.set(item, 'sqlite:////%s/%s' % (self.user_config_path, parser.get('main', item)))
        for item in ['sleep_time']:
            self.set(item, parser.getint('main', item))
        for item in ['ignore_keywords']:
            self.set(item, map(lambda x: unicode(x.decode('utf-8')).lower(), parser.get('main', item).split(',')))

    def get(self, item):
        """ Fetches config item from the list. """
        if item in self.config.keys():
            return self.config[item]
        return None


if __name__ == '__main__':
    Config()
