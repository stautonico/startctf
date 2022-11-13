from threading import Thread
import argparse

from startctfutil.tools import Tool, run
from startctfutil.args import get_arg
from startctfutil.io import info, warn


class Nmap(Tool):
    # TODO: Docstring
    def __init__(self, name: str, description: str, parser: argparse.ArgumentParser):
        super().__init__(name, description, parser)

    def run(self) -> Thread:
        # TODO: Docstring
        if get_arg("ip"):
            command = f"{self.tool_path} {get_arg('ip')} -v"

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

            return run(command, f"nmap - {get_arg('ip')}")
        else:
            warn("No IP address provided, skipping nmap scan.")


    def parse_output(self, file: str) -> None:
        """
        Parse the output of the tool and add it to the README.md (simply a stub, should be overridden by subclasses)
        """
        raise NotImplementedError(f"parse_output() not implemented for {self.name}")
