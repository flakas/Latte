import argparse
import textwrap

class Arguments:
    def __init__(self, args):
        self.args = args
        self.parsed = {}

        self.build_parser()

    def get(self, key):
        return getattr(self.parsed, key)

    def parse(self):
        self.parsed = self.parser.parse_args()

    def build_parser(self):
        parser = argparse.ArgumentParser(
            description=self.get_description(),
            formatter_class=argparse.RawTextHelpFormatter
        )

        parser = self.register_time_arguments(parser)

        parser.add_argument('-g', metavar='GROUPING', choices=['title', 'instance', 'class'], help='Group entries by: title, instance or class')
        parser.add_argument('-o', metavar='ORDERING', choices=['asc', 'desc'], help='Order entries by duration: asc or desc')

        parser = self.register_display_arguments(parser)

        parser.set_defaults(
            g='title',
            o='desc',
        )

        self.parser = parser

    def register_time_arguments(self, parser):
        print('registering group')
        time_group = parser.add_mutually_exclusive_group()
        time_group.add_argument('--time-all', const='all', action='store_const', help='Analyze all known log data')
        time_group.add_argument('--time-seconds', metavar='S', type=int, help='Analyze log data created in last S seconds')
        time_group.add_argument('--time-days', metavar='D', type=int, help='Analyze log data created in last D days')
        time_group.add_argument('--time-weeks', metavar='W', type=int, help='Analyze log data created in last W weeks')
        time_group.add_argument('--time-months', metavar='M', type=int, help='Analyze log data created in last M months')

        return parser

    def register_display_arguments(self, parser):
        display_group = parser.add_mutually_exclusive_group()
        display_group.add_argument('--display-all', const='all', action='store_const', help='Display all found entries in the chosen time interval')
        display_group.add_argument('--display-limit', type=int, metavar='N', help='Display up to N top entries')
        display_group.add_argument('--display-share', type=int, metavar='PERCENTAGE', help='Display entries that have a share of the analyzed logs greater than SHARE, where SHARE is any number between 0 and 100')
        display_group.add_argument('--display-time', type=int, metavar='SECONDS', help='Display entries that have the accumulated time greater than SECONDS')

        return parser


    def get_description(self):
        return textwrap.dedent('''
            Linux automatic time tracker

            Tracks time spent on activities based on window titles.
            Data files are saved to ~/.config/latte (by default, configurable)

            More information:
            https://github.com/flakas/Latte
            ''')
