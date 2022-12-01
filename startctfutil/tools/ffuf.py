import os
from json import load
from threading import Thread

from startctfutil.arg_parser import get_arg
from startctfutil.config import read_config_key
from startctfutil.io import warn
from startctfutil.markdown import make_url
from startctfutil.markdown.table import Table
from startctfutil.readme import README, ReadmeSection, HeadingLevel
from startctfutil.shared import STATE
from startctfutil.tools import Tool, run


# TODO: Find a better way to do this
# group = arg_parser.add_argument_group("ffuf")
# group.add_argument("--ffuf-args", type=str, help="Extra arguments to pass to ffuf", default="")


class ffuf(Tool):
    # TODO: Docstring
    def __init__(self, port):
        super().__init__("ffuf", "Fast web fuzzer written in Go")
        self.port = port

    def run(self) -> Thread:
        # TODO: Docstring
        wordlist = read_config_key("tools", "webscanner_wordlist")
        if not os.path.exists(wordlist):
            # This is so that only a single warning is printed (instead of one for each web service)
            if STATE.get("failed_fuff"):
                return Thread(target=lambda: None)
            else:
                STATE["failed_fuff"] = True
            warn(f"Wordlist not found at {wordlist}, skipping ffuf.")
            return Thread(target=lambda: None)

        self.make_log_dir()

        command = f"{self.tool_path} -u http://{get_arg('ip')}:{self.port}/FUZZ -w {wordlist} -o logs/ffuf/{self.port}.json -of json {get_arg('ffuf_args')}"
        return run(command, f"fuff - {get_arg('ip')}:{self.port}")

    def parse_output(self) -> None:
        # TODO: Docstring
        with open(f"logs/ffuf/{self.port}.json", "r") as f:
            data = load(f)

        if not data.get("results"):
            return

        show_content_type = read_config_key("output", "show_content_type")
        show_size = read_config_key("output", "show_size")

        table_headers = ["Path", "Status"]
        if show_content_type:
            table_headers.append("Content-Type")
        if show_size:
            table_headers.append("Size")

        table = Table(table_headers)
        for result in data["results"]:
            row = [
                make_url("/" + result["input"]["FUZZ"], result["url"]),
                result["status"]
            ]
            if show_content_type:
                row.append(result["content-type"])
            if show_size:
                row.append(result["length"])

            table.add_row(row)

        section = ReadmeSection(f"Discovered Web Paths (:{self.port})", HeadingLevel.H3)
        section.add_content(table.render())

        README.add_section(section)
