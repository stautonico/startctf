import os

from startctfutil.scripts import Script, download_file
from startctfutil.io import warn


class winpeas(Script):
    def __init__(self):
        super().__init__(
            name="winpeas",
            description="A script that searches for possible local privilege escalation paths that you could exploit and print them to you with nice colors so you can recognize the misconfigurations easily.",
            repo_url="https://github.com/carlospolop/PEASS-ng",
        )

    def obtain(self) -> bool:
        print("Download exe or bat file? (exe/bat)")
        while True:
            selection = input("> ").lower()
            if selection in ["exe", "bat"]:
                break
            else:
                warn("Invalid selection, please try again.")

        try:
            if selection == "exe":
                content = download_file(
                    f"https://github.com/carlospolop/PEASS-ng/releases/latest/download/winpeasany.exe")
            else:
                content = download_file(
                    f"https://github.com/carlospolop/PEASS-ng/releases/latest/download/winpeas.bat")

            if content is None:
                return False

            with open(f"scripts/winpeas.{selection}", "wb") as f:
                f.write(content)

            return True

        except Exception as e:
            warn(f"Failed to download file: {e}")
            return False
