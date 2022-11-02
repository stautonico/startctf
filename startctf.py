#!/usr/bin/env python3
import argparse
import os
from configparser import ConfigParser
from datetime import datetime
from threading import Thread
from xml.dom import minidom

current_user = os.getlogin()
home_dir = os.popen(f"eval ech3"
                    f"o ~{current_user}").read().replace("\n", "")

config_dir = os.path.join(home_dir, ".startctf")

config = ConfigParser()

config.read(os.path.join(config_dir, "ctf.conf"))

arg_parser = argparse.ArgumentParser(description="Create a CTF template")

arg_parser.add_argument("name", type=str, help="The name of the ctf (also the name of the created dir)")

arg_parser.add_argument("--ip", help="The ip address of the target server")

arg_parser.add_argument("-nS", "--net-scan", help="Run a simple nmap scan", action="store_true")
arg_parser.add_argument("-nSA", "--net-scan-all", help="Run an nmap scan and scan all ports", action="store_true")
arg_parser.add_argument("-Pn", help="Includes the -Pn flag to the nmap scan (skip ping)", action="store_true")

arg_parser.add_argument("-e4l", "--enum4linux", help="Run an enum4linux scan on the host", action="store_true")


def create_template(name):
    # First check if the directory exists
    if os.path.exists(f"./{name}"):
        print(f"Folder with the name {name} already exists")
        exit(1)

    # Make the directory that will hold the ctf files
    os.mkdir(f"./{name}")

    os.chdir(f"./{name}")

    # Find the user's network mapper (nmap by default)
    network_scanner = config.get("tools", "net_scanner").split("/")[-1]

    # Create the directory that holds the net map scans
    os.mkdir(network_scanner)

    # Make the xml directory (for xml out/internal parsing)
    os.mkdir(os.path.join(network_scanner, "xml"))

    # Make the directory for storing logs (from enum tools etc)
    os.mkdir("logs")

    # Make the directory for exfiltrated documents
    os.mkdir("exfiltrated_docs")

    # Make directory for scripts/exploits/etc
    os.mkdir("scripts")


def create_readme(name, ip=None):
    person_name = config.get("title", "name")
    date = datetime.now().strftime("%b/%d/%Y")
    readme = f"""#### {person_name} - {date}\n
# {name}
---\n

### Files
---\n

### Creds
---\n
"""

    if ip:
        readme += f"\n### Info\n---\nIP Address: {ip}\n"

    with open("README.md", "w") as f:
        f.write(readme)


def run_nmap(args):
    os.popen(" ".join(args)).read()


def nmap_scan(ip, mode="default", pn=False):
    nmap_args = ["nmap", "-sV", "-v", ip]
    if pn:
        nmap_args.append("-Pn")
    if mode == "default":
        nmap_args.append("-oN")
        nmap_args.append("nmap/initial")
        # Also output the xml for internal processing
        nmap_args.append("-oX")
        nmap_args.append("nmap/xml/initial.xml")
        thread = Thread(target=run_nmap, args=[nmap_args])
        thread.start()
        return thread
    if mode == "all":
        nmap_args.append("-A")
        nmap_args.append("-p-")
        nmap_args.append("-oN")
        nmap_args.append("nmap/all_ports")
        # Also output the xml for internal processing
        nmap_args.append("-oX")
        nmap_args.append("nmap/xml/all_ports.xml")
        thread = Thread(target=run_nmap, args=[nmap_args])
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
            service = port.childNodes[1]

            port_number = port.attributes["portid"].value
            port_status = state.attributes["state"].value
            service_name = service.attributes["name"].value

            f.write(f"| {port_number} | {port_status} | {service_name} |\n")


def enum_4_linux(ip):
    os.popen(f"enum4linux -a {ip} | tee logs/enum4linux.log").read()


if __name__ == '__main__':
    has_ip = False
    running_nmap = False
    default_nmap_thread = None
    all_nmap_thread = None
    enum_4_linux_thread = None

    args = arg_parser.parse_args()

    create_template(args.name)
    try:
        create_readme(args.name, args.ip)
        has_ip = True
    except AttributeError:
        create_readme(args.name)

    # Check if we should run nmap scans
    if has_ip:
        if args.net_scan:
            default_nmap_thread = nmap_scan(args.ip, pn=args.Pn)
            running_nmap = True

        if args.net_scan_all:
            all_nmap_thread = nmap_scan(args.ip, mode="all", pn=args.Pn)
            running_nmap = True
    else:
        if args.net_scan or args.net_scan_all:
            print("Unable to run nmap scans, no IP provided")

    if args.enum4linux:
        enum_4_linux_thread = Thread(target=enum_4_linux, args=[args.ip])
        enum_4_linux_thread.start()

    if running_nmap:
        print("Waiting for nmap scan(s) to finish")
        if default_nmap_thread:
            default_nmap_thread.join()
            # Parse the output once its one
            if not all_nmap_thread:
                parse_nmap_output("nmap/xml/initial.xml")
        if all_nmap_thread:
            all_nmap_thread.join()
            # Parse the output once its one
            parse_nmap_output("nmap/xml/all_ports.xml")

    if enum_4_linux_thread:
        print(f"Waiting for enum4linux to finish")
        enum_4_linux_thread.join()


# TODO: add new section to the README.md (Web directories)
