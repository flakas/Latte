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
        self.set('user_inactive_threshold', 6 * 60)
        self.set('analyzer_output_default', '- [%s::%s] "%s" : %s')
        self.set('analyzer_output_title', '- "%s": %s')
        self.set('analyzer_output_class', '- "%s": %s')
        self.set('analyzer_output_instance', '- "%s": %s')

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
        for item in ['sleep_time', 'user_inactive_threshold']:
            self.set(item, parser.getint('main', item))
        for item in ['ignore_keywords']:
            self.set(item, map(lambda x: unicode(x.decode('utf-8')).lower(), parser.get('main', item).split(',')))
        for item in ['analyzer_output_default', 'analyzer_output_title', 
        'analyzer_output_class', 'analyzer_output_instance']:
            self.set(item, parser.get('main', item))
        for item in ['aliases']:
            aliases_dict = {}
            aliases = map(lambda y: y.split(':'), parser.get('main', item).split(','))
            for alias in aliases:
                l = map(lambda x: unicode(x.decode('utf-8')), alias)
                aliases_dict[l[0]] = l[1]
            self.set('aliases', aliases_dict)

    def get(self, item):
        """ Fetches config item from the list. """
        if item in self.config.keys():
            return self.config[item]
        return None


if __name__ == '__main__':
    Config()
