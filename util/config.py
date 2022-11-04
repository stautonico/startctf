from .shared import CONFIG
import os
from . import HOME_DIR
from .color import Colors, colorize
from configparser import ConfigParser

# TODO: Add cli arg of location to config

CONFIG_PATH = os.getenv("STARTCTF_CONFIG_PATH") or os.path.join(HOME_DIR, ".config", "startctf", "ctf.conf")

def read_config_key(section, key, default=None):
    try:
        return CONFIG.get(section, key)
    except Exception:
        return default


# This needs to be down here to prevent circular imports
from .io import warn

# Make sure the config exists
if not os.path.exists(CONFIG_PATH):
    print("Config file not found, creating one now...")
    CONFIG.read_string("")
    warn(f"Config file not found, using default values.")
    # print(
    #     f"[{colorize('FAIL', Colors.FG.RED, {'bold': True})}] {colorize(f'Config file not found at {CONFIG_PATH}', Colors.FG.RED, {'bold': True})}")
    # exit(1)
else:
    # Load the config
    CONFIG.read(CONFIG_PATH)

# if len(CONFIG.sections()) == 0:
#     print(
#         f"[{colorize('FAIL', Colors.FG.RED, {'bold': True})}] {colorize(f'Failed to read configuration file', Colors.FG.RED, {'bold': True})}")
#     exit(1)
