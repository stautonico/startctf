from typing import List


class Table:
    """
    A helper class that allows easy generation of tables in Markdown.
    """

    def __init__(self, headers: List[str]):
        self.headers: List[str] = headers
        self.rows: List[List[str]] = []

    def add_row(self, row: List[str]) -> None:
        """
        Add a row to the table.

        Args: row: A list of strings that will be added as a row to the table. (The length of the list must be equal
        to the number of headers)
        """
        if len(row) != len(self.headers):
            raise ValueError("The length of the row must be equal to the number of headers.")

        self.rows.append(row)

    def render(self) -> str:
        """
        Render the table as a Markdown table.

        Returns:
            The Markdown table.
        """
        return str(self)

    def __str__(self):
        output = "| " + " | ".join(self.headers) + " |\n"
        output += "| " + " | ".join(["---"] * len(self.headers)) + " |\n"
        for row in self.rows:
            output += "| " + " | ".join(row) + " |\n"
        return output
