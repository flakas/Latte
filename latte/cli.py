from latte.parsers import main_parser, run_parser, stats_parser
from latte.commands import Analyzer, Monitor
from latte.config import Config
from latte.core import Core

def main(argv=None):
    parser = main_parser()
    options, rest = parser.parse_known_args()

    if not options.command:
        parser.print_help()
        return

    core = Core()

    if options.command == 'run':
        Monitor(core.config, core.get_db(), run_parser().parse_args(rest).silent).run()
    elif options.command == 'stats':
        Analyzer(core.config, core.get_db(), stats_parser().parse_args(rest)).run()
