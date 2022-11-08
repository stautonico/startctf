#!/usr/bin/env python3
from startctfutil.args import parse_args, get_arg
from startctfutil.config import init_config
from startctfutil.files import create_directory_template, create_readme_template, parse_nmap_output
from startctfutil.io import info, success
from startctfutil.tools import run_nmap_scan


def main():
    parse_args()
    init_config()
    # TODO: Add ability to use rustscan instead of nmap
    # TODO: Move tools to their own file (or tools/nmap.py, etc)
    # TODO: Move most of everything else to their own files, this file should only be a main function
    # TODO: REWRITE THE INSTALLATION SCRIPT
    # TODO: REWRITE THE UNINSTALLATION SCRIPT
    # TODO: Add a version to the config file so if future versions change the config format,
    #      the user can be notified and the config file can be updated
    # TODO: Use type hints everywhere

    # Create the directory template
    create_directory_template(get_arg("name"))

    # Create the README template
    create_readme_template(get_arg("name"), get_arg("ip"))

    if not get_arg("silent_tools"):
        info("Note: Spawned xterm windows may be stacked on top of each other, move them around to see them all")

    nmap_thread = None

    # If we have any of the operation arguments, run the tools
    if get_arg("nmap_scan"):
        nmap_thread = run_nmap_scan()

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

    success("All done, get to pwning!")


if __name__ == '__main__':
    main()
