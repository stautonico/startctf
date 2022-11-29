import sys
from argparse import ArgumentParser, Namespace

from startctfutil.arg_parser import merge_args, ARG_PARSER
from startctfutil.io import info
from startctfutil.scripts import SUPPORTED_SCRIPTS


def internal_command_scripts(parent_args: Namespace):
    # TODO: Docstring
    parser = ArgumentParser(description="Download/generate third-party scripts",
                            add_help=False,
                            usage="""startctf scripts [<args>])""")

    parser.add_argument("-l", "--list", "--list-scripts", action="store_true",
                        help="List all supported 3rd party scripts that can be downloaded/generated",
                        required=False)

    args = merge_args(parser.parse_args(sys.argv[2:]), parent_args)

    if args.list:
        info("Supported scripts:")
        for script in SUPPORTED_SCRIPTS:
            info(f"  {script}")
        exit(0)
    else:
        print("TODO: Download/generate scripts or parse subargs")
        exit(0)


def load_commands():
    ARG_PARSER.add_command("scripts", internal_command_scripts)
    ARG_PARSER.add_command("script", internal_command_scripts)
