import argparse
import textwrap

def main_parser():
    description = textwrap.dedent('''
    Latte time tracker

    This runs activity logger and tracks time spent on activities based on window titles.
    Data files are saved to ~/.config/latte (default, but configurable)

    To check usage statistics run `latte stats` command.

    More information:
    https://github.com/flakas/Latte''')

    parser = argparse.ArgumentParser(
            prog='latte',
            description=description,
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('command', choices=['run', 'stats', 'tags'], action='store', help='latte command')

    return parser

def run_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--silent', action='store_true', help='Silence all output from latte')

    return parser

def stats_parser():
    description = textwrap.dedent('''
    Linux automatic time tracker

    Tracks time spent on activities based on window titles.
    Data files are saved to ~/.config/latte (by default, configurable)

    More information:
    https://github.com/flakas/Latte
    ''')

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter
    )

    time_group = parser.add_mutually_exclusive_group()
    time_group.add_argument('--time-all', const='all', action='store_const', help='Analyze all known log data')
    time_group.add_argument('--time-seconds', metavar='S', type=int, help='Analyze log data created in last S seconds')
    time_group.add_argument('--time-days', metavar='D', type=int, help='Analyze log data created in last D days')
    time_group.add_argument('--time-weeks', metavar='W', type=int, help='Analyze log data created in last W weeks')
    time_group.add_argument('--time-months', metavar='M', type=int, help='Analyze log data created in last M months')

    parser.add_argument('-g', metavar='GROUPING', choices=['title', 'instance', 'class'], help='Group entries by: title, instance or class')
    parser.add_argument('-o', metavar='ORDERING', choices=['asc', 'desc'], help='Order entries by duration: asc or desc')

    display_group = parser.add_mutually_exclusive_group()
    display_group.add_argument('--display-all', const='all', action='store_const', help='Display all found entries in the chosen time interval')
    display_group.add_argument('--display-limit', type=int, metavar='N', help='Display up to N top entries')
    display_group.add_argument('--display-share', type=int, metavar='PERCENTAGE', help='Display entries that have a share of the analyzed logs greater than SHARE, where SHARE is any number between 0 and 100')
    display_group.add_argument('--display-time', type=int, metavar='SECONDS', help='Display entries that have the accumulated time greater than SECONDS')

    parser.add_argument('--tags', default='', help='Comma-separated tag names to filter to')

    parser.set_defaults(
        g='title',
        o='desc',
    )

    return parser

def tags_parser():
    description = textwrap.dedent('''
    Linux automatic time tracker

    Tracks time spent on activities based on window titles.
    Data files are saved to ~/.config/latte (by default, configurable)

    More information:
    https://github.com/flakas/Latte
    ''')

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='subcommand', help='subcommands')
    tags_retag_parser(subparsers)
    tags_add_parser(subparsers)
    tags_delete_parser(subparsers)
    tags_show_parser(subparsers)

    return parser

def tags_retag_parser(parent):
    parser = parent.add_parser('retag', help='Add a tag')

def tags_add_parser(parent):
    parser = parent.add_parser('add', help='Add a tag')
    parser.add_argument('name', action='store', help='Tag name')
    parser.add_argument('--window-title', action='store', dest='window_title', help='Window title case-insensitive regex')
    parser.add_argument('--window-class', action='store', dest='window_class', help='Window class case-insensitive regex')
    parser.add_argument('--window-instance', action='store', dest='window_instance', help='Window instance case-insensitive regex')
    return parser

def tags_delete_parser(parent):
    parser = parent.add_parser('delete', help='Delete a tag')
    parser.add_argument('name', action='store', help='Tag name')

def tags_show_parser(parent):
    parser = parent.add_parser('show', help='Show all tags')
