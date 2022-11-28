import os
import shutil

from startctfutil.io import error
from startctfutil.args import get_arg


def create_directory_template(name):
    force = get_arg("force")

    # First, check if the directory exists
    if os.path.exists(name):
        if force:
            # If the force flag is set, delete the directory
            shutil.rmtree(name)
        else:
            error(f"A directory with the name {name} already exists")
            exit(1)

    # Create the directory that will hold the ctf files
    os.mkdir(name)
    os.chdir(name)

    # Create the startctf hidden directory that contains information/settings about the current CTF
    os.mkdir(".startctf")

    # Make the directory for storing logs (from enum tools etc.)
    os.mkdir("logs")

    # Make the directory for exfiltrated documents
    os.mkdir("exfiltrated_docs")

    # Make directory for scripts/exploits/etc
    os.mkdir("scripts")
