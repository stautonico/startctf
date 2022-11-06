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

from startctfutil.args import parse_args, get_arg
from startctfutil.files import create_directory_template, create_readme_template, parse_nmap_output
from startctfutil.io import info, success
from startctfutil.tools import run_nmap_scan, run_enum4linux


def main():
    parse_args()
    # global ARGS
    # TODO: Add ability to use rustscan instead of nmap
    # TODO: Move tools to their own file (or tools/nmap.py, tools/enum4linux.py, etc)
    # TODO: Move most of everything else to their own files, this file should only be a main function
    # TODO: REWRITE THE INSTALLATION SCRIPT
    # TODO: REWRITE THE UNINSTALLATION SCRIPT
    # TODO: Add a version to the config file so if future versions change the config format,
    #      the user can be notified and the config file can be updated

    # Create the directory template
    create_directory_template(get_arg("name"))

    # Create the README template
    create_readme_template(get_arg("name"), get_arg("ip"))

    if not get_arg("silent_tools"):
        info("Note: Spawned xterm windows may be stacked on top of each other, move them around to see them all")

    nmap_thread = None
    enum4linux_thread = None

    # If we have any of the operation arguments, run the tools
    if get_arg("nmap_scan"):
        nmap_thread = run_nmap_scan()

    if get_arg("enum4linux"):
        enum4linux_thread = run_enum4linux()

    # Wait for the threads to finish
    if nmap_thread:
        info("Waiting for nmap to finish...")
        nmap_thread.join()
        success("Nmap finished")

        # Parse the nmap output
        if get_arg("nmap_all"):
            parse_nmap_output("nmap/xml/all_ports.xml")
        else:
            parse_nmap_output("nmap/xml/initial.xml")

    if enum4linux_thread:
        info("Waiting for enum4linux to finish...")
        enum4linux_thread.join()
        success("Enum4linux finished")

    success("All done, get to pwning!")


if __name__ == '__main__':
    main()
