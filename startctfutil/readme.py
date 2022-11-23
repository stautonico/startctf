from typing import Dict
from enum import Enum
from datetime import datetime

from startctfutil.config import read_config_key
from startctfutil import is_true


class HeadingLevel(Enum):
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    H5 = 5
    H6 = 6


class ReadmeSection:
    # TODO: Add docstring
    def __init__(self, title: str, heading_level: HeadingLevel):
        self.title: str = title
        self.heading_level: HeadingLevel = heading_level
        self.content: str = ""

    def add_content(self, content: str):
        # TODO: Add docstring
        self.content += content

    def render(self) -> str:
        # TODO: Add docstring
        # noinspection PyTypeChecker
        output = f"{'#' * self.heading_level.value} {self.title}\n"
        output += self.content
        return output


class Readme:
    # TODO: Add docstring
    def __init__(self, path: str):
        self.path: str = path
        self.sections: Dict[str, ReadmeSection] = {}

    def add_section(self, section: ReadmeSection) -> None:
        # TODO: Add docstring
        self.sections[section.title] = section

    def remove_section(self, title: str) -> None:
        # TODO: Docstring
        if title in self.sections:
            del self.sections[title]

    def render(self) -> str:
        # TODO: Add docstring
        output = ""
        for section in self.sections.values():
            output += section.render() + "\n\n"
        return output

    def write(self) -> None:
        # TODO: Add docstring
        author_name = read_config_key("meta", "author")

        if read_config_key("meta", "use_day_month_year", "false"):
            date = datetime.now().strftime("%d/%m/%Y")
        else:
            date = datetime.now().strftime("%m/%d/%Y")

        output = f"""> {author_name} - {date}\n\n"""
        output += self.render()

        with open(self.path, "w") as f:
            f.write(output)


# Global README object
README = Readme("README.md")
