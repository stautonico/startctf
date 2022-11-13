from typing import Dict
from enum import Enum


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

    def render(self) -> str:
        # TODO: Add docstring
        # noinspection PyTypeChecker
        output = f"{'#' * self.heading_level.value} {self.title}\n"
        output += self.content
        # noinspection PyTypeChecker
        return f"{'#' * self.heading_level.value} {self.title}"


class Readme:
    # TODO: Add docstring
    def __init__(self, path: str):
        self.path: str = path
        self.sections: Dict[str, ReadmeSection] = {}

    def add_section(self, section: ReadmeSection) -> None:
        # TODO: Add docstring
        self.sections[section.title] = section

    def render(self) -> str:
        # TODO: Add docstring
        output = ""
        for section in self.sections.values():
            output += section.render() + "\n\n"
        return output

    def write(self) -> None:
        # TODO: Add docstring
        with open(self.path, "w") as f:
            f.write(self.render())
