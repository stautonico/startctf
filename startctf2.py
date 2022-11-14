#!/usr/bin/env python3
import os

from startctfutil.args import parse_args, get_arg, set_arg
from startctfutil.config import init_config
from startctfutil.files import create_directory_template, create_readme_template, parse_nmap_output, parse_ffuf_output
from startctfutil.io import info, success, warn
# from startctfutil.tools import run_nmap_scan, auto_scan
from startctfutil.readme import README, ReadmeSection, HeadingLevel
from startctfutil.tools.nmap import Nmap


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
    # TODO: Add option to overwrite existing files
    # TODO: Add option to disable tables in generated READMEs

    # Create the directory template
    create_directory_template(get_arg("name"))

    README.add_section(ReadmeSection(get_arg("name"), HeadingLevel.H1))

    # Create the README template
    # create_readme_template(get_arg("name"), get_arg("ip"))

    if not get_arg("silent_tools"):
        info("Note: Spawned xterm windows may be stacked on top of each other, move them around to see them all")

    nmap_thread = None

    if (not get_arg("nmap_scan") and not get_arg("nmap_all")) and get_arg("auto_scan"):
        warn("Auto scan requires a nmap scan, ignoring auto scan...")
        set_arg("auto_scan", False)

    nmap = None
    # If we have any of the operation arguments, run the tools
    if get_arg("nmap_scan"):
        nmap = Nmap()
        nmap_thread = nmap.run()

    # Wait for the threads to finish
    if nmap_thread:
        info("Waiting for nmap to finish...")
        nmap_thread.join()
        success("Nmap finished")

        # Parse the nmap output
        if get_arg("nmap_all"):
            nmap.parse_output("logs/nmap/xml/all_ports.xml")
        else:
            nmap.parse_output("logs/nmap/xml/initial.xml")

        # if get_arg("auto_scan"):
        #     threads = auto_scan()
        #     for port, data in threads.items():
        #         info(f"Waiting for {data['tool']} on port {port} to finish...")
        #         thread = data.get("thread")
        #         if thread:
        #             thread.join()
        #             success(f"{data['tool']} on port {port} finished")
        #
        #     if len(threads) > 0:
        #         # TODO: Do this better
        #         for file in os.listdir("logs/ffuf"):
        #             if file.endswith(".json"):
        #                 parse_ffuf_output(f"logs/ffuf/{file}")

    README.write()

    success("All done, get to pwning!")


if __name__ == '__main__':
    main()
