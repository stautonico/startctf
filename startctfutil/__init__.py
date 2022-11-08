import os
import subprocess

__author__ = "Steve Tautonico"
__copyright__ = "Copyright 2022, Steve Tautonico"
__credits__ = ["Steve Tautonico"]
__license__ = "MIT"
__version__ = "2.0"


def run_command_and_get_output(command, strip=False):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        if strip:
            result = result.strip()
        return result
    except subprocess.CalledProcessError as e:
        result = e.output.decode("utf-8")
        if strip:
            result = result.strip()
        return result


CURRENT_USER = os.getlogin()
HOME_DIR = os.path.expanduser("~")

CONFIG_DEFAULT_VALUES = {
    "meta": {
        "author": CURRENT_USER,
        "use_day_month_year": "false",
    },
    "tools": {
        "nmap": run_command_and_get_output("which nmap", strip=True) or None,
        "rustscan": run_command_and_get_output("which rustscan", strip=True) or None,
    },
    "output": {
        "emojis": "true",
        "include_field_templates": "true",
    }
}


# Misc functions go here
def is_true(value):
    if value is None:
        return False
    return value.lower() in ("yes", "true", "t", "1")


def is_false(value):
    if value is None:
        return False
    return value.lower() in ("no", "false", "f", "0")
