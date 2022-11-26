import argparse

from startctfutil import __version__, __author__

ARGS = None


# Custom argparser so that we can customize it if we need
class ArgParser(argparse.ArgumentParser):
    pass


arg_parser = ArgParser(description="Create a CTF template and automate some common tasks")

arg_parser.add_argument("name", type=str, help="The name of the ctf (also the name of the created dir)",
                        nargs="?")

arg_parser.add_argument("--ip", help="The ip address of the target server", required=False)

# Operation arguments
arg_parser.add_argument("-nS", "--nmap-scan", action="store_true", help="Run a simple nmap scan on the given ip")

arg_parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing files (careful, destructive)",
                        default=False)

# TODO: Add more tools
arg_parser.add_argument("-as", "--auto-scan", action="store_true",
                        help="Try to detect which services are running on the target and run the appropriate tools (-nS or -nSA required)")

# Settings
# TODO: Maybe add option to not popout new xterm windows
arg_parser.add_argument("--install-manpage", action="store_true",
                        help="Downloads and installs the manpage (requires sudo/root)")

arg_parser.add_argument("-s", "--silent", action="store_true",
                        help="Don't show any output from any of the tools or the script itself")

arg_parser.add_argument("-st", "--silent-tools", action="store_true",
                        help="Only silence output from tools, but still show status messages")

arg_parser.add_argument("-nw", "--no-warnings", action="store_true",
                        help="Don't show any warnings from the script")

arg_parser.add_argument("-V", "--version",
                        action="version",
                        version=f"startctf v{__version__} by {__author__}\n(https://github.com/stautonico/startctf)")


def parse_args():
    global ARGS
    ARGS = arg_parser.parse_args()

    # If we don't have name, or install-manpage, we need to show the usage
    # We don't need to handle help or version because argparse does that for us
    for arg in ["name", "install_manpage"]:
        if getattr(ARGS, arg) is not None and getattr(ARGS, arg) is not False:
            break
    else:
        arg_parser.print_usage()
        exit(1)


def get_arg(name, default=None):
    global ARGS
    return ARGS.__dict__.get(name, default)


def set_arg(name, value):
    # This should only be used in specific circumstances
    global ARGS
    ARGS.__dict__[name] = value
