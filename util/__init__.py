import os

__author__ = "Steve Tautonico"
__copyright__ = "Copyright 2022, Steve Tautonico"
__credits__ = ["Steve Tautonico"]
__license__ = "MIT"
__version__ = "2.0"

CURRENT_USER = os.getlogin()
HOME_DIR = os.path.expanduser("~")

# Misc functions go here
def is_true(value):
    if value is None:
        return False
    return value.lower() in ("yes", "true", "t", "1")


def is_false(value):
    if value is None:
        return False
    return value.lower() in ("no", "false", "f", "0")
