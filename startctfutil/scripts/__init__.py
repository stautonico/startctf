from typing import Optional
import requests

SUPPORTED_SCRIPTS = ["linpeas", "winpeas"] # TODO: Support winpeas

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

    def __init__(self, name: str, description: str, repo_url: Optional[str] = None):
        self.name: str = name
        self.description: str = description
        self.repo_url: Optional[str] = repo_url

    def download(self) -> bool:
        """
        Download the script (simply a stub, should be overridden by subclasses)
        Returns:
            downloaded: `True` if the script was downloaded, `False` otherwise
        """
        raise NotImplementedError(f"download() not implemented for {self.name}")

    def compile(self) -> bool:
        """
        If the script needs to be compiled, compile it (simply a stub, should be overridden by subclasses)
        Returns:
            compiled: `True` if the script was compiled, `False` otherwise
        """
        return False
