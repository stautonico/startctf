from typing import Optional

import requests

# TODO: Don't hardcode the scripts directory, use the path module?
SUPPORTED_SCRIPTS = ["linpeas", "winpeas", "reverse_shell"]


def download_file(url: str) -> bytes:
    """
    Download a file from a URL

    Args:
        url: The URL to download the file from

    Returns:
        content: The content of the downloaded file
    """
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Failed to download file from '{url}'")

    return r.content


class Script:
    """
    A generic script class that can be used to create new third-party script utilities.
    This class should be subclasses to implement new third-party scripts.
    A script is a third-party utility that can be downloaded (into the "scripts" folder)
    Each script should implement the `download()` method and may implement the `compile()` method.
    """

    def __init__(self, name: str, description: str, repo_url: Optional[str] = None, prints_messages: bool = False):
        self.name: str = name
        self.description: str = description
        self.repo_url: Optional[str] = repo_url
        self.prints_messages = prints_messages

    def obtain(self) -> bool:
        """
        Generate or download the script (simply a stub, should be overridden by subclasses)
        Returns:
            success: `True` if the script was obtained, `False` otherwise
        """
        raise NotImplementedError(f"download() not implemented for {self.name}")
