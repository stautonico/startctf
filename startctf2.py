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
from datetime import datetime

__author__ = "Steve Tautonico"
__copyright__ = "Copyright 2022, Steve Tautonico"
__credits__ = ["Steve Tautonico"]
__license__ = "MIT"
__version__ = "2.0"


# This may be ugly, but I don"t want to have multiple files to make it easy to install
# All utilities will be in this single file. Maybe I"ll split it up later

def is_true(value):
    return value.lower() in ("yes", "true", "t", "1")


def is_false(value):
    return value.lower() in ("no", "false", "f", "0")


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

ARGS = None  # Our global parsed ARGS so everything can use it


def error(text):
    # TODO: Check the config file if we should print emojis
    if not ARGS.silent:
        print(f"[{colorize('💀', Colors.FG.RED, {'bold': True})}] {colorize(text, Colors.FG.RED, {'bold': True})}")


def info(text):
    if not ARGS.silent:
        print(f"[{colorize('ℹ️', Colors.FG.BLUE, {'bold': True})}] {colorize(text, Colors.FG.BLUE)}")


def success(text):
    if not ARGS.silent:
        print(f"[{colorize('✅', Colors.FG.GREEN, {'bold': True})}] {colorize(text, Colors.FG.GREEN)}")


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

arg_parser.add_argument("-V", "--version",
                        action="version",
                        version=f"startctf v{__version__} by {__author__}\n(https://github.com/stautonico/startctf)")


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
    author_name = config.get("meta'", "author") or current_user
    date = datetime.now().strftime("%m/%d/%Y")
    readme = f"""#### {author_name} - {date}

# {ctf_name}
---
### Files
---
[remote]/home/foo/bar.txt - Some file that contains text
[local, in exfiltrated_docs]baz.txt - Some file that contains text

### Creds
---
username:password - Some credentials for ssh @someip
"""

    if ip:
        readme += f"""\n### Host(s) Info\n---\nIP Address: {ip}\n"""

    with open("README.md", "w") as f:
        f.write(readme)


def run_command_in_xterm(command, title):
    os.system(f"xterm -T \"{title}\" -e \"{command}\"")


def run_command_in_background(command):
    os.system(f"{command}")


def run_nmap_scan():
    if ARGS.ip:
        command = f"nmap {ARGS.ip} -v"

        if ARGS.nmap_Pn:
            command += " -Pn"

        if not ARGS.no_sV:
            command += " -sV"

        if ARGS.nmap_all:
            command += " -p- -oN nmap/all_ports.nmap -oX nmap/xml/all_ports.xml"
        else:
            command += " -oN nmap/initial.nmap -oX nmap/xml/initial.xml"

        # TODO: Change this message based on the verbosity level
        info(f"Running nmap scan on {ARGS.ip}")

        if ARGS.silent:
            thread = Thread(target=run_command_in_background, args=(command,))
        else:
            thread = Thread(target=run_command_in_xterm, args=(command, f"nmap - {ARGS.ip}"))

        thread.start()
        return thread


def run_enum4linux():
    # TODO: Implement
    return None


if __name__ == '__main__':
    # TODO: Add ability to use rustscan instead of nmap
    ARGS = arg_parser.parse_args()

    # Create the directory template
    create_directory_template(ARGS.name)

    # Create the README template
    create_readme_template(ARGS.name, ARGS.ip)

    nmap_thread = None
    enum4linux_thread = None

    # If we have any of the operation arguments, run the tools
    if ARGS.nmap_scan:
        nmap_thread = run_nmap_scan()

    if ARGS.enum4linux:
        enum4linux_thread = run_enum4linux()

    # Wait for the threads to finish
    if nmap_thread:
        info("Waiting for nmap to finish...")
        nmap_thread.join()

    if enum4linux_thread:
        info("Waiting for enum4linux to finish...")
        enum4linux_thread.join()

    success("All done, get to pwning!")
