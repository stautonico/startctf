from . import __version__, __author__
import argparse

# from .shared import ARGS

ARGS = None

arg_parser = argparse.ArgumentParser(description="Create a CTF template")

arg_parser.add_argument("name", type=str, help="The name of the ctf (also the name of the created dir)")

arg_parser.add_argument("--ip", help="The ip address of the target server", required=False)

# Operation arguments
arg_parser.add_argument("-nS", "--nmap-scan", action="store_true", help="Run a simple nmap scan on the given ip")

arg_parser.add_argument("-nSA", "--nmap-all", action="store_true",
                        help="Run a full nmap scan on the given ip (all ports, slow)")

arg_parser.add_argument("-Pn", "--nmap-Pn", action="store_true",
                        help="Run a nmap scan with the -Pn flag (skip host discovery)")

arg_parser.add_argument("-nSV", "--no-sV", action="store_true",
                        help="Don't run nmap with the -sV flag (don't detect service versions)")

# TODO: Add more arguments for e4l
arg_parser.add_argument("-e4l", "--enum4linux", action="store_true", help="Run enum4linux on the given ip")

# TODO: Add more tools

# Settings
# TODO: Maybe add option to not popout new xterm windows
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
    print(ARGS)

# def set_args(parsed_args):
#     global ARGS
#     ARGS = parsed_args


def get_arg(name, default=None):
    global ARGS
    return ARGS.__dict__.get(name, default)
    # return arg_parser.parse_args().__dict__.get(name, default)
