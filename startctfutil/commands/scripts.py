import importlib
import os
import sys
from argparse import ArgumentParser, Namespace

from startctfutil.arg_parser import merge_args
from startctfutil.io import info, error, success
from startctfutil.scripts import SUPPORTED_SCRIPTS


def command_scripts(parent_args: Namespace):
    # TODO: Docstring
    parser = ArgumentParser(description="Download/generate third-party scripts",
                            add_help=False,
                            usage="""startctf scripts [<args>])""")

    parser.add_argument("script", help="The script to download/generate", choices=SUPPORTED_SCRIPTS, nargs="?")

    parser.add_argument("-l", "--list", "--list-scripts", action="store_true",
                        help="List all supported 3rd party scripts that can be downloaded/generated",
                        required=False)

    args = merge_args(parser.parse_args(sys.argv[2:]), parent_args)

    if args.list:
        info("Supported scripts:")
        for script in SUPPORTED_SCRIPTS:
            info(f"  {script}")
        exit(0)

    if args.script is None:
        error("No script specified")
        exit(1)

    if not os.path.exists(".startctf"):
        error("You must be in a startctf directory to download a script.")
        exit(1)

    to_download = args.script
    if to_download is None:
        error("You must specify a script to download.")
        exit(1)

    if to_download not in SUPPORTED_SCRIPTS:
        error(f"Script '{to_download}' is not supported. Use --list to see a list of supported scripts.")
        exit(1)


    info(f"Obtaining script '{to_download}'...")
    try:
        script_module = importlib.import_module(f"startctfutil.scripts.{to_download}")
        script = getattr(script_module, to_download)()
        result = script.obtain()
        if result:
            if not script.prints_messages:
                success(f"Script '{to_download}' downloaded successfully!")
            exit(0)
        else:
            if not script.prints_messages:
                error(f"Failed to download script '{to_download}'.")
            exit(1)
    except ModuleNotFoundError:
        error(f"Script '{to_download}' not found. Please open an issue on GitHub.")
        exit(1)
    except Exception as e:
        error(f"Failed to download script '{to_download}'. Please open an issue on GitHub. (Error: {e})")
