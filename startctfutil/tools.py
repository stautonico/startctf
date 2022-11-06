import os
import subprocess
from .args import get_arg
from threading import Thread
from .io import info


def run_command_in_xterm(command, title):
    os.system(f"xterm -T \"{title}\" -e \"{command}\"")


def run_command_in_background(command):
    # Run commands silently in the background with popen
    subprocess.call(command, shell=True, stdout=subprocess.PIPE)


def run_nmap_scan():
    # print(f"Args in our nmap scan: {ARGS}")
    if get_arg("ip"):
        command = f"nmap {get_arg('ip')} -v"

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


def run_enum4linux():
    if get_arg("ip"):
        command = f"enum4linux -a {get_arg('ip')} | tee logs/enum4linux.log"
        # TODO: Change this message based on the verbosity level
        info(f"Running enum4linux scan on {get_arg('ip')}")

        if get_arg("silent") or get_arg("silent_tools"):
            thread = Thread(target=run_command_in_background, args=(command,))
        else:
            thread = Thread(target=run_command_in_xterm, args=(command, f"enum4linux - {ARGS.ip}"))

        thread.start()
        return thread
