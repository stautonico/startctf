import os
from threading import Thread

from startctfutil.arg_parser import get_arg
from startctfutil.config import read_config_key
from startctfutil.io import warn
from startctfutil.shared import STATE
from startctfutil.tools import Tool, run


def make_args(args_group):
    args_group.add_argument("--gobuster-args", type=str, help="Extra arguments to pass to gobuster", default="")


class gobuster(Tool):
    # TODO: Docstring
    def __init__(self, port):
        super().__init__("gobuster", "Directory/file & DNS busting tool")
        self.port = port

    def run(self) -> Thread:
        # TODO: Docstring
        wordlist = read_config_key("tools", "webscanner_wordlist")
        if not os.path.exists(wordlist):
            # This is so that only a single warning is printed (instead of one for each web service)
            if STATE.get("failed_gobuster"):  # TODO: Find a way to do this globally rather than per tool
                return Thread(target=lambda: None)
            else:
                STATE["failed_gobuster"] = True
            warn(f"Wordlist not found at {wordlist}, skipping gobuster.")
            return Thread(target=lambda: None)

        self.make_log_dir()

        # TODO: Make the scheme configurable (or try to auto-detect it)
        command = f"{self.tool_path} dir -u http://{get_arg('ip')}:{self.port} -w {wordlist} -o logs/gobuster/{self.port}.log {get_arg('gobuster_args')}"

        print(command)

        return run(command, f"{self.name} - {get_arg('ip')}:{self.port}")

    def parse_output(self, file: str) -> None:
        warn("gobuster output parsing not implemented yet")
        return
