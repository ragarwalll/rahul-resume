"""Configuration for table formatting"""

from dataclasses import dataclass
from typing import List

__all__ = ["TableConfig"]


@dataclass
class TableConfig:
    """Configuration for table formatting"""

    environment: str = "tabular"
    column_format: str = "l"
    row_separator: str = "\n"
    column_separator: str = " & "
    row_end: str = " \\\\"
    begin: str = "\\begin{tabular}{rll}"
    end: str = "\\end{tabular}"

    def wrap_in_environment(self, content: str) -> str:
        """Wrap content in LaTeX environment"""
        return f"{self.begin}%\n{content}%\n{self.end}"

    def format_row(self, cells: List[str], escape_latex: callable) -> str:
        """Format row with cells"""
        cells = [escape_latex(cell) for cell in cells]
        return f"{self.column_separator.join(cells)}{self.row_end}"

    def format_table(self, rows: List[List[str]], escape_latex: callable) -> str:
        """Format table with rows"""
        return self.row_separator.join(
            self.format_row(row, escape_latex) for row in rows
        )
