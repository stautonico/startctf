#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2022 Steve Tautonico

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
from configparser import ConfigParser
import argparse
from threading import Thread
import os
from datetime import datetime

__author__ = "Steve Tautonico"
__copyright__ = "Copyright 2022, Steve Tautonico"
__credits__ = ["Steve Tautonico"]
__license__ = "MIT"
__version__ = "2.0"


# This may be ugly, but I don"t want to have multiple files to make it easy to install
# All utilities will be in this single file. Maybe I"ll split it up later
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[01m"
    DISABLE = "\033[02m"
    UNDERLINE = "\033[04m"
    REVERSE = "\033[07m"
    STRIKETHROUGH = "\033[09m"
    INVISIBLE = "\033[08m"

    class FG:
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        ORANGE = "\033[33m"
        BLUE = "\033[34m"
        PURPLE = "\033[35m"
        CYAN = "\033[36m"
        LIGHT_GREY = "\033[37m"
        DARK_GREY = "\033[90m"
        LIGHT_RED = "\033[91m"
        LIGHT_GREEN = "\033[92m"
        YELLOW = "\033[93m"
        LIGHT_BLUE = "\033[94m"
        PINK = "\033[95m"
        LIGHT_CYAN = "\033[96m"

    class BG:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        ORANGE = "\033[43m"
        BLUE = "\033[44m"
        PURPLE = "\033[45m"
        CYAN = "\033[46m"
        LIGHTGREY = "\033[47m"


DEFAULT_COLOR_MODIFIERS = {
    "bold": False,
    "underline": False,
    "reverse": False,
    "strikethrough": False,
    "invisible": False
}


def colorize(text, color, modifiers=None):
    if modifiers is None:
        modifiers = DEFAULT_COLOR_MODIFIERS

    output = color

    if modifiers.get("bold"):
        output += Colors.BOLD
    if modifiers.get("underline"):
        output += Colors.UNDERLINE
    if modifiers.get("reverse"):
        output += Colors.REVERSE
    if modifiers.get("strikethrough"):
        output += Colors.STRIKETHROUGH
    if modifiers.get("invisible"):
        output += Colors.INVISIBLE

    output += text + Colors.RESET

    return output


def error(text):
    # TODO: Check the config file if we should print emojis
    print(f"[{colorize('💀', Colors.FG.RED, {'bold': True})}] {colorize(text, Colors.FG.RED, {'bold': True})}")


current_user = os.getlogin()
home_dir = os.path.expanduser("~")

CONFIG_PATH = os.getenv("STARTCTF_CONFIG_PATH") or os.path.join(home_dir, ".config", "startctf", "ctf.conf")

# Make sure the config exists
if not os.path.exists(CONFIG_PATH):
    # This print error is different because we don't have the config yet
    print(
        f"[{colorize('FAIL', Colors.FG.RED, {'bold': True})}] {colorize(f'Config file not found at {CONFIG_PATH}', Colors.FG.RED, {'bold': True})}")
    exit(1)

# Load the config
config = ConfigParser()
config.read(CONFIG_PATH)
if len(config.sections()) == 0:
    print(
        f"[{colorize('FAIL', Colors.FG.RED, {'bold': True})}] {colorize(f'Failed to read configuration file', Colors.FG.RED, {'bold': True})}")
    exit(1)

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
arg_parser.add_argument("--silent", "-s", action="store_true", help="Don't show any output from any of the tools")


def create_directory_template(name):
    # First, check if the directory exists
    if os.path.exists(name):
        error(f"A directory with the name {name} already exists")
        exit(1)

    # Create the directory that will hold the ctf files
    os.mkdir(name)
    os.chdir(name)

    # Make the directory to store nmap scan results
    os.mkdir("nmap")
    os.mkdir("nmap/xml")  # XML output

    # Make the directory for storing logs (from enum tools etc)
    os.mkdir("logs")

    # Make the directory for exfiltrated documents
    os.mkdir("exfiltrated_docs")

    # Make directory for scripts/exploits/etc
    os.mkdir("scripts")


def create_readme_template(ctf_name, ip=None):
    author_name = config.get("meta", "author") or current_user
    date = datetime.now().strftime("%m/%d/%Y")
    readme = f"""#### {author_name} - {date}\n

# {ctf_name}
---\n

### Files
--- \n
[remote]/home/foo/bar.txt - Some file that contains text
[local, in exfiltrated_docs]baz.txt - Some file that contains text

### Creds
---\n
username:password - Some credentials for ssh @someip
"""

    if ip:
        readme += f"""\n### Host(s) Info\n---\nIP Address: {ip}\n"""

    with open("README.md", "w") as f:
        f.write(readme)


if __name__ == '__main__':
    args = arg_parser.parse_args()

    # Create the directory template
    create_directory_template(args.name)

    # Create the README template
    create_readme_template(args.name, args.ip)

# def code():
#     os.system('xterm -e bash -c \"python /tmp/newbruh.py; exit\"')
#
# br = Thread(target=code)
# br2 = Thread(target=code)
#
# br.start()
# br2.start()
# br.join()
# br2.join()
