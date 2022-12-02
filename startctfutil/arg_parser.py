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
        self.parsed_args: Optional[Namespace] = None
        self.root_parser = ArgumentParser(description="Create a CTF template and automate some common tasks",
                                          add_help=False,
                                          usage="""startctf <command> [<args>]

Available commands:
    start | new     Create a new CTF template
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
                                      help="Don't show any output from any of the tools or the script itself",
                                      default=False)

        self.root_parser.add_argument("--install-manpage", action="store_true",
                                      help="Downloads and installs the manpage (requires sudo/root)")

        self.root_parser.add_argument("-V", "--version",
                                      action="version",
                                      version=f"startctf v{__version__} by {__author__}\n(https://github.com/stautonico/startctf)")

        self.root_parser.add_argument("--help", "-h", help="Show this help message and exit", action="store_true")

        self.root_parser.add_argument("--debug", "-d", help="Prints debug information", action="store_true")

    def _parse_args(self):
        # Skip the first argument (the script name)
        self.parsed_args = self.root_parser.parse_known_args(sys.argv[1:])[0]

        if self.parsed_args.help and not self.parsed_args.command:
            self.root_parser.print_usage()
            sys.exit(0)

    def add_command(self, command, handler):
        self.command_handlers[command] = handler

    def _run(self):
        # Call subcommand by name
        handler = self.command_handlers.get(get_arg("command"))
        if not handler:
            # TODO: Change this message
            print("[DEBUG] Unrecognized command")
            self.root_parser.print_usage()
            exit(1)

        handler()

    def get_arg(self, arg, default=None):
        return getattr(self.parsed_args, arg, default)

    def set_arg(self, arg, value):
        setattr(self.parsed_args, arg, value)

    def append_args(self, args):
        self.parsed_args = merge_args(self.parsed_args, args)


ARG_PARSER = ArgParser()


# TODO: Add docstrings for the below
def parse_args():
    global ARG_PARSER
    ARG_PARSER._parse_args()


def run():
    ARG_PARSER._run()


def set_args(args: Namespace):
    """
    Set the global arguments

    Args:
        args: The arguments to set
    """
    global ARG_PARSER
    ARG_PARSER.append_args(args)


def get_arg(name: str, default=None) -> Optional[str]:
    """
    Get an argument from the parsed arguments

    Args:
        name: The name of the argument
        default: The default value if the argument is not found

    Returns:
        The argument value
    """
    global ARG_PARSER
    return ARG_PARSER.get_arg(name, default)


def set_arg(name: str, value):
    """
    Set an argument. Should only be used in special cases

    Args:
        name: The name of the argument
        value: The value to set
    """
    global ARG_PARSER
    ARG_PARSER.set_arg(name, value)
