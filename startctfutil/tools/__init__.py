import os
import subprocess
from threading import Thread
import argparse
from typing import List

from startctfutil.args import get_arg
from startctfutil.io import info, warn
from startctfutil.config import read_config_key
from startctfutil.files import parse_nmap_output_to_object
from startctfutil.shared import STATE


class Tool:
    """
    A generic tool class that can be used to create new tools.
    This class should be subclassed to create new tools.
    A tool is a program that can be run on the target server.
    Each tool should implement the `run()` and `parse_output()` methods.
    """

    def __init__(self, name: str, description: str, parser: argparse.ArgumentParser):
        self.name: str = name
        self.description: str = description
        self.parser: argparse.ArgumentParser = parser

        self.tool_path = self.check_tool_path()

    def run(self) -> Thread:
        """
        Execute the tool (simply a stub, should be overridden by subclasses)
        """
        raise NotImplementedError(f"run() not implemented for {self.name}")

    def parse_output(self, file: str) -> None:
        """
        Parse the output of the tool and add it to the README.md (simply a stub, should be overridden by subclasses)
        """
        raise NotImplementedError(f"parse_output() not implemented for {self.name}")

    def check_tool_path(self) -> bool:
        """
        Check if the tool path is set in the config file. Otherwise, check the default path.
        If the tool is not found, warn the user and return False.

        Returns:
            exists: `True` if the tool is found, `False` otherwise
        """
        tool_path = read_config_key("tools", self.name)
        if not os.path.exists(tool_path):
            if tool_path is None:
                warn(f"{self.name.title()} not found, please install it or set the path in the config.")
            else:
                warn(
                    f"{self.name.title()} not found at '{tool_path}', please install it or set the path in the config.")

            return False

        return tool_path


def run_command_in_xterm(command: str, title: str) -> None:
    """
    Run a command in an xterm window

    Args:
        command: The command to run
        title: The title of the xterm window
    """
    os.system(f"xterm -T \"{title}\" -e \"{command}\"")


def run_command_in_background(command: str) -> None:
    """
    Run a command in the background

    Args:
        command: The command to run
    """
    subprocess.call(command, shell=True, stdout=subprocess.PIPE)


def run(command: str, title: str) -> Thread:
    """
    A wrapper function that automatically decides which method to use to run a command.
    If the `silent` or `silent_tools` argument is set, the command will be run in the background.
    Otherwise, it will be run in an xterm window.
    The thread is started and returned.

    Args:
        command: The command to run
        title: The title of the xterm window

    Returns:
        thread: The thread that is running the command
    """
    if get_arg("silent") or get_arg("silent_tools"):
        thread = Thread(target=run_command_in_background, args=(command,))
    else:
        thread = Thread(target=run_command_in_xterm, args=(command, title))

    thread.start()
    return thread
