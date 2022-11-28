import os

from startctfutil.scripts import Script, download_file
from startctfutil.io import warn


class linpeas(Script):
    """
    Linpeas is a script that can be used to enumerate a linux system.
    """

    def __init__(self):
        super().__init__(
            name="linpeas",
            description="A script that searches for possible local privilege escalation paths that you could exploit and print them to you with nice colors so you can recognize the misconfigurations easily.",
            repo_url="https://github.com/carlospolop/PEASS-ng",
        )

    def download(self) -> bool:
        try:
            content = download_file("https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh")
            if content is None:
                return False

            with open("scripts/linpeas.sh", "wb") as f:
                f.write(content)

            # Make the script executable
            os.chmod("scripts/linpeas.sh", 0o755)

            return True

        except Exception as e:
            warn(f"Failed to download linpeas: {e}")
            return False
