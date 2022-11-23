import os
from configparser import ConfigParser

from startctfutil import HOME_DIR, CONFIG_DEFAULT_VALUES, is_true, is_false

# TODO: Add cli arg of location to config


CONFIG = ConfigParser()  # Parsed config object

CONFIG_PATH = os.getenv("STARTCTF_CONFIG_PATH") or os.path.join(HOME_DIR, ".config", "startctf", "ctf.conf")


def read_config_key(section, key, default=None, ):
    try:
        result = CONFIG.get(section, key)
    except Exception:
        result = CONFIG_DEFAULT_VALUES.get(section, {}).get(key, default)

    if is_true(result):
        return True
    elif is_false(result):
        return False
    else:
        return result


def init_config():
    # We have to import this to prevent circular imports
    from startctfutil.io import warn
    # Make sure the config exists
    if not os.path.exists(CONFIG_PATH):
        CONFIG.read_string("")
        # print(CONFIG.sections())
        warn(f"Config file not found, using default values.")
    else:
        # Load the config
        CONFIG.read(CONFIG_PATH)
