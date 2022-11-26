import os
import subprocess
from threading import Thread
from typing import Literal, Optional
import importlib

from startctfutil.args import get_arg
from startctfutil.io import warn
from startctfutil.config import read_config_key
from startctfutil.shared import STATE

SUPPORTED_TOOLS = {
    "network_scanner": ["nmap"],  # TODO: rustscan
    "web_fuzzer": ["ffuf", "gobuster"]
}


def get_preferred_tool(category: Literal["network_scanner", "web_fuzzer"]) -> Optional[str]:
    """
    Get the preferred tool for a category (from the config file)

    Args:
        category: The category to get the preferred tool for

    Returns:
        tool: The name preferred tool
    """
    if category not in SUPPORTED_TOOLS:
        raise ValueError(f"Invalid category '{category}'")

    find_alternative = False

    preferred_tool = read_config_key("tools", f"preferred_{category}")
    if preferred_tool not in SUPPORTED_TOOLS[category]:
        warn(f"Invalid preferred tool '{preferred_tool}' for category '{category}' (not supported)")
        find_alternative = True
    else:
        # Confirm that the preferred tool is installed
        tool_path = read_config_key("tools", preferred_tool)
        if not os.path.exists(tool_path):
            warn(
                f"{preferred_tool.title()} not found at '{tool_path}', please install it or set the path in the config.")
            find_alternative = True

    # TODO: Find a way to do this without checking twice
    if find_alternative:
        # Try to find an alternative tool
        other_tools = SUPPORTED_TOOLS[category].copy()
        if preferred_tool in other_tools:  # If it's not, that means the user tried to set an invalid tool (which is already handled)
            other_tools.remove(preferred_tool)

        for tool in other_tools:
            warn(f"Trying {tool} instead...")
            tool_path = read_config_key("tools", tool)
            if os.path.exists(tool_path):
                warn(f"Using {tool.title()} instead")
                STATE["tools"][category] = tool
                return tool

        warn(f"Could not find any other tools for category '{category}'")
        STATE["tools"][category] = "Not found"
        return None
    else:
        STATE["tools"][category] = preferred_tool
        return preferred_tool


def try_import_preferred_tool(category: Literal["network_scanner", "web_fuzzer"]):
    """
    Try to import the preferred tool for a category.

    Args:
        category: The category to import the preferred tool for
    """
    # Try to see if the state already cached this
    if category in STATE.get("tools", {}):
        if STATE["tools"][category] == "Not found":
            return None
        else:
            tool = STATE["tools"][category]
    else:
        tool = get_preferred_tool(category)
        if tool is None:
            return None

    try:
        tool_module = importlib.import_module(f"startctfutil.tools.{tool}")
    except ModuleNotFoundError:
        return None

    return getattr(tool_module, tool)


class Tool:
    """
    A generic tool class that can be used to create new tools.
    This class should be subclassed to create new tools.
    A tool is a program that can be run on the target server.
    Each tool should implement the `run()` and `parse_output()` methods.
    """

    def __init__(self, name: str, description: str):
        self.name: str = name
        self.description: str = description

        self.tool_path = self.check_tool_path()

    def run(self) -> Thread:
        """
        Execute the tool (simply a stub, should be overridden by subclasses)
        """
        raise NotImplementedError(f"run() not implemented for {self.name}")

    def make_log_dir(self) -> None:
        """
        Create a log directory to store the tools log files (if it doesn't already exist)
        """
        if not os.path.exists(f"logs/{self.name}"):
            os.mkdir(f"logs/{self.name}")

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
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


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
