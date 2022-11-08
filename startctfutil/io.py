from startctfutil.color import Colors, colorize
from startctfutil import is_true
from startctfutil.config import read_config_key
from startctfutil.args import get_arg


# TODO: Add option in config to output message in white text
# TODO: Add option in config to disable colored output
# TODO: Add option to use long info for output ("SUCCESS" instead of "+", "FAIL" instead of "X")

def error(text):
    if not get_arg("silent"):
        if is_true(read_config_key("output", "emojis", "true")):
            print(f"[{colorize('💀', Colors.FG.RED, {'bold': True})}] {colorize(text, Colors.FG.RED)}")
        else:
            print(f"[{colorize('X', Colors.FG.RED, {'bold': True})}] {colorize(text, Colors.FG.RED)}")


def warn(text):
    if not get_arg("silent", "false") and not get_arg("no_warnings", "false"):
        if is_true(read_config_key("output", "emojis", "true")):
            print(f"[{colorize('⚠️', Colors.FG.YELLOW, {'bold': True})}] {colorize(text, Colors.FG.YELLOW)}")
        else:
            print(f"[{colorize('~', Colors.FG.YELLOW, {'bold': True})}] {colorize(text, Colors.FG.YELLOW)}")


def info(text):
    if not get_arg("silent", "false"):
        if is_true(read_config_key("output", "emojis", "true")):
            print(f"[{colorize('ℹ️', Colors.FG.BLUE, {'bold': True})}] {colorize(text, Colors.FG.BLUE)}")
        else:
            print(f"[{colorize('*', Colors.FG.BLUE, {'bold': True})}] {colorize(text, Colors.FG.BLUE)}")


def success(text):
    if not get_arg("silent", "false"):
        if is_true(read_config_key("output", "emojis", "true")):
            print(f"[{colorize('✅', Colors.FG.GREEN, {'bold': True})}] {colorize(text, Colors.FG.GREEN)}")
        else:
            print(f"[{colorize('+', Colors.FG.GREEN, {'bold': True})}] {colorize(text, Colors.FG.GREEN)}")
