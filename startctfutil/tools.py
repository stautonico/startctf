import os
import subprocess
from threading import Thread

from startctfutil.args import get_arg
from startctfutil.io import info, warn
from startctfutil.config import read_config_key


def run_command_in_xterm(command, title):
    os.system(f"xterm -T \"{title}\" -e \"{command}\"")


def run_command_in_background(command):
    # Run commands silently in the background with popen
    subprocess.call(command, shell=True, stdout=subprocess.PIPE)


def run_nmap_scan():
    # print(f"Args in our nmap scan: {ARGS}")
    if get_arg("ip"):
        # Check if we can find nmap
        nmap_path = read_config_key("tools", "nmap")

        # TODO: Maybe make this an error (and exit)  rather than a warning?
        if not os.path.exists(nmap_path):
            if nmap_path is None:
                warn("Nmap not found, please install it or set the path in the config.")
            else:
                warn(f"Nmap not found at '{nmap_path}', please install it or set the path in the config.")

            return

        command = f"{nmap_path} {get_arg('ip')} -v"

        if get_arg("nmap_Pn"):
            command += " -Pn"

        if not get_arg("no_sV"):
            command += " -sV"

        if get_arg("nmap_all"):
            command += " -p- -oN nmap/all_ports.nmap -oX nmap/xml/all_ports.xml"
        else:
            command += " -oN nmap/initial.nmap -oX nmap/xml/initial.xml"

        # TODO: Change this message based on the verbosity level
        info(f"Running nmap scan on {get_arg('ip')}")

        if get_arg("silent") or get_arg("silent_tools"):
            thread = Thread(target=run_command_in_background, args=(command,))
        else:
            thread = Thread(target=run_command_in_xterm, args=(command, f"nmap - {get_arg('ip')}"))

        thread.start()
        return thread

    else:
        warn("No IP address provided, skipping nmap scan.")