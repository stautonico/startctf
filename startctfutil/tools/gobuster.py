from threading import Thread
import os
from json import load

from startctfutil.tools import Tool, run
from startctfutil.config import read_config_key
from startctfutil.args import get_arg, arg_parser
from startctfutil.io import warn
from startctfutil.readme import README, ReadmeSection, HeadingLevel
from startctfutil.markdown.table import Table
from startctfutil.markdown import make_url
from startctfutil.shared import STATE

# TODO: Find a better way to do this
group = arg_parser.add_argument_group("gobuster")

group.add_argument("--gobuster-args", type=str, help="Extra arguments to pass to gobuster", default="")


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
