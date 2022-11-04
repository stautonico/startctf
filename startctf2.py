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
from threading import Thread
from datetime import datetime
from xml.dom import minidom
import subprocess

from util import CURRENT_USER, is_true
from util.args import arg_parser
from util.config import read_config_key
from util.io import error, info, success
from util.shared import CONFIG, ARGS


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
    os.mkdir("tools")


def create_readme_template(ctf_name, ip=None):
    author_name = read_config_key("meta", "author", CURRENT_USER)

    if is_true(read_config_key("meta", "use_day_month_year", "false")):
        date = datetime.now().strftime("%d/%m/%Y")
    else:
        date = datetime.now().strftime("%m/%d/%Y")

    # TODO: Make this not so fucking ugly
    readme = f"""> {author_name} - {date}\n# {ctf_name}\n---\n"""
    if is_true(CONFIG.get("output", "include_field_templates")):
        readme += "A short description of the CTF goes here\n\n"

    readme += """\n### Files\n---\n\n"""

    if is_true(CONFIG.get("output", "include_field_templates")):
        # Remove the last newline
        readme = readme[:-1]
        readme += """[remote]/home/foo/bar.txt - Some file that contains text
[local, in exfiltrated_docs]baz.txt - Some file that contains text\n\n\n"""
    readme += """### Creds\n---\n"""

    if is_true(CONFIG.get("output", "include_field_templates")):
        readme += """username:password - Some credentials for ssh @someip\n\n"""

    if ip:
        readme += f"""\n### Host(s) Info\n---\nIP Address: {ip}"""

    with open("README.md", "w") as f:
        f.write(readme)


def run_command_in_xterm(command, title):
    os.system(f"xterm -T \"{title}\" -e \"{command}\"")


def run_command_in_background(command):
    # Run commands silently in the background with popen
    subprocess.call(command, shell=True, stdout=subprocess.PIPE)
    # p.communicate()
    # subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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

        if ARGS.silent or ARGS.silent_tools:
            thread = Thread(target=run_command_in_background, args=(command,))
        else:
            thread = Thread(target=run_command_in_xterm, args=(command, f"nmap - {ARGS.ip}"))

        thread.start()
        return thread


def run_enum4linux():
    if ARGS.ip:
        command = f"enum4linux -a {ARGS.ip} | tee logs/enum4linux.log"
        # TODO: Change this message based on the verbosity level
        info(f"Running enum4linux scan on {ARGS.ip}")

        if ARGS.silent or ARGS.silent_tools:
            thread = Thread(target=run_command_in_background, args=(command,))
        else:
            thread = Thread(target=run_command_in_xterm, args=(command, f"enum4linux - {ARGS.ip}"))

        thread.start()
        return thread


def parse_nmap_output(output_file):
    result = minidom.parse(output_file)
    ports = result.getElementsByTagName("port")

    with open("README.md", "a") as f:
        f.write("\n### Ports\n---\n")
        # Write the headers
        f.write("| Port | Status | Service |\n")
        f.write("|:----:|:------:|:-------:|\n")
        for port in ports:
            state = port.childNodes[0]
            try:
                service = port.childNodes[1]
            except IndexError:
                service = None

            port_number = port.attributes["portid"].value
            port_status = state.attributes["state"].value
            if service:
                service_name = service.attributes["name"].value
            else:
                service_name = "unknown"

            f.write(f"| {port_number} | {port_status} | {service_name} |\n")


if __name__ == '__main__':
    # TODO: Add ability to use rustscan instead of nmap
    # TODO: Move tools to their own file (or tools/nmap.py, tools/enum4linux.py, etc)
    # TODO: Move most of everything else to their own files, this file should only be a main function
    ARGS = arg_parser.parse_args()

    # Create the directory template
    create_directory_template(ARGS.name)

    # Create the README template
    create_readme_template(ARGS.name, ARGS.ip)

    if not ARGS.silent_tools:
        info("Note: Spawned xterm windows may be stacked on top of each other, move them around to see them all")

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
        success("Nmap finished")

        # Parse the nmap output
        if ARGS.nmap_all:
            parse_nmap_output("nmap/xml/all_ports.xml")
        else:
            parse_nmap_output("nmap/xml/initial.xml")

    if enum4linux_thread:
        info("Waiting for enum4linux to finish...")
        enum4linux_thread.join()
        success("Enum4linux finished")

    success("All done, get to pwning!")
