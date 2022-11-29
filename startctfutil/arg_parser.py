# Thanks Chase Seibert, this is alot better than using argparse on its own
# https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
import sys
from argparse import ArgumentParser, Namespace
from typing import Optional

from startctfutil import __version__, __author__

ARGS = None


def merge_args(a: Namespace, b: Namespace) -> Namespace:
    """
    Marge two namespaces

    Args:
        a: The first namespace
        b: The second namespace

    Returns:
        The merged namespace
    """
    return Namespace(**{**vars(a), **vars(b)})


class ArgParser:
    """
    Our custom argparser class that can handle subcommands and sub-arguments
    """

    def __init__(self):
        self.root_parser = ArgumentParser(description="Create a CTF template and automate some common tasks",
                                          add_help=False,
                                          usage="""startctf <command> [<args>]

Available commands:
    new     Create a new CTF template
    scripts Download/generate third-party scripts

Other options:
    -h, --help - Prints this help message
    -v, --version - Prints the version of startctf
    -d, --debug - Prints debug information (not implemented)
""")
        self.command_handlers = {
        }

        self.root_parser.add_argument("command", help="Subcommand to run", nargs="?")

        self.root_parser.add_argument("-nw", "--no-warnings", action="store_true",
                                      help="Don't show any warnings from the script")

        self.root_parser.add_argument("-s", "--silent", action="store_true",
                                help="Don't show any output from any of the tools or the script itself")

        self.root_parser.add_argument("--install-manpage", action="store_true",
                                      help="Downloads and installs the manpage (requires sudo/root)")

        self.root_parser.add_argument("-V", "--version",
                                      action="version",
                                      version=f"startctf v{__version__} by {__author__}\n(https://github.com/stautonico/startctf)")

        self.root_parser.add_argument("--help", "-h", help="Show this help message and exit", action="store_true")

        self.root_parser.add_argument("--debug", "-d", help="Prints debug information", action="store_true")

    def _parse_args(self):
        global ARGS
        ARGS = self.root_parser.parse_known_args(sys.argv[1:])[0]

        args_for_subcommand = Namespace(help=ARGS.help, debug=ARGS.debug)

        if ARGS.help and not ARGS.command:
            self.root_parser.print_usage()
            sys.exit(0)

        # Call subcommand by name
        handler = self.command_handlers.get(ARGS.command)
        if not handler:
            print("[DEBUG] Unrecognized command")
            self.root_parser.print_usage()
            exit(1)

        handler(args_for_subcommand)

    def add_command(self, command, handler):
        self.command_handlers[command] = handler



ARG_PARSER = ArgParser()


def parse_args():
    global ARGS
    global ARG_PARSER
    ARGS = ARG_PARSER._parse_args()


def get_arg(name: str, default=None) -> Optional[str]:
    """
    Get an argument from the parsed arguments

    Args:
        name: The name of the argument
        default: The default value if the argument is not found

    Returns:
        The argument value
    """
    global ARGS
    return getattr(ARGS, name, default)


def set_arg(name: str, value):
    """
    Set an argument. Should only be used in special cases

    Args:
        name: The name of the argument
        value: The value to set
    """
    global ARGS
    setattr(ARGS, name, value)
