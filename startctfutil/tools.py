import os
import subprocess
from threading import Thread

from startctfutil.args import get_arg
from startctfutil.io import info, warn
from startctfutil.config import read_config_key
from startctfutil.files import parse_nmap_output_to_object
from startctfutil.shared import STATE


def run_command_in_xterm(command, title):
    os.system(f"xterm -T \"{title}\" -e \"{command}\"")


def run_command_in_background(command):
    # Run commands silently in the background with popen
    subprocess.call(command, shell=True, stdout=subprocess.PIPE)


def run(command, title):
    if get_arg("silent") or get_arg("silent_tools"):
        thread = Thread(target=run_command_in_background, args=(command,))
    else:
        thread = Thread(target=run_command_in_xterm, args=(command, title))

    thread.start()
    return thread


def check_tool_path(tool: str):
    # Check if we can find nmap
    tool_path = read_config_key("tools", tool)
    if not os.path.exists(tool_path):
        if tool_path is None:
            warn(f"{tool.title()} not found, please install it or set the path in the config.")
        else:
            warn(f"{tool.title()} not found at '{tool_path}', please install it or set the path in the config.")

        return False

    return True


def run_nmap_scan():
    if get_arg("ip"):
        has_nmap = check_tool_path("nmap")
        if not has_nmap:
            return

        command = f"{read_config_key('tools', 'nmap')} {get_arg('ip')} -v"

        if get_arg("nmap_Pn"):
            command += " -Pn"

        if not get_arg("no_sV"):
            command += " -sV"

        if get_arg("nmap_all"):
            command += " -p- -oN logs/nmap/all_ports.nmap -oX logs/nmap/xml/all_ports.xml"
        else:
            command += " -oN logs/nmap/initial.nmap -oX logs/nmap/xml/initial.xml"

        # TODO: Change this message based on the verbosity level
        info(f"Running nmap scan on {get_arg('ip')}")

        thread = run(command, f"nmap - {get_arg('ip')}")
        return thread

    else:
        warn("No IP address provided, skipping nmap scan.")


def run_feroxbuster_scan(port):
    has_feroxbuster = check_tool_path("feroxbuster")
    if not has_feroxbuster:
        return

    wordlist = read_config_key("tools", "directory_list")
    if not os.path.exists(wordlist):
        if STATE.get("failed_feroxbuster"):
            return
        else:
            STATE["failed_feroxbuster"] = True
        warn(f"Directory list not found at '{wordlist}', please set the path in the config.")
        return

    tool_path = read_config_key("tools", "feroxbuster")

    command = f"{tool_path} --url http://{get_arg('ip')}:{port} --wordlist {wordlist} --json --output logs/feroxbuster/{port}.json -k"

    thread = run(command, f"feroxbuster - {get_arg('ip')}:{port}")
    return thread


def auto_scan():
    # TODO: Find a way to get this result without having to re-parse the nmap output
    if get_arg("nmap_all"):
        nmap_output = "logs/nmap/xml/all_ports.xml"
    else:
        nmap_output = "logs/nmap/xml/initial.xml"

    result = parse_nmap_output_to_object(nmap_output)
    threads = {}

    for port, info in result.items():
        # TODO: Check this is a more thorough and reliable way
        if info["status"] == "open":
            if "http" in info["service"]:
                # TODO: Support gobuster
                threads[port] = {
                    "tool": "feroxbuster",
                    "thread": run_feroxbuster_scan(port)
                }

    return threads
