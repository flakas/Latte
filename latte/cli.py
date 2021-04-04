from latte.parsers import main_parser, run_parser, stats_parser
from latte.latte import Latte
from latte.analyzer.Analyzer import Analyzer
from latte.Config import Config

def main(argv=None):
    parser = main_parser()
    options, rest = parser.parse_known_args()

    if not options.command:
        parser.print_help()
        return

    if options.command == 'run':
        Latte(run_parser().parse_args(rest).silent).run()
    elif options.command == 'stats':
        Analyzer(Config(), Latte().get_session(), stats_parser().parse_args(rest)).run()
