from .shared import CONFIG
import os
from . import HOME_DIR, CONFIG_DEFAULT_VALUES

# TODO: Add cli arg of location to config

CONFIG_PATH = os.getenv("STARTCTF_CONFIG_PATH") or os.path.join(HOME_DIR, ".config", "startctf", "ctf.conf")


def read_config_key(section, key, default=None):
    try:
        return CONFIG.get(section, key)
    except Exception:
        return CONFIG_DEFAULT_VALUES.get(section, {}).get(key, default)


# This needs to be down here to prevent circular imports
from . import io

# Make sure the config exists
if not os.path.exists(CONFIG_PATH):
    print("Config file not found, creating one now...")
    CONFIG.read_string("")
    io.warn(f"Config file not found, using default values.")
else:
    # Load the config
    CONFIG.read(CONFIG_PATH)
