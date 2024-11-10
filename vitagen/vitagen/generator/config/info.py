"""Info configuration."""

from dataclasses import dataclass
from vitagen.generator.config.base import DisplayMode

__all__ = ["InfoFormatConfig"]


@dataclass
class InfoFormatConfig:
    """Configuration for info text formatting"""

    pipe_separator: str = "|"
    space_separator: str = " "
    new_line: str = "\\newline%\n"
    command: str = "\\info"

    def get_prefix(self, mode: DisplayMode) -> str:
        """Get appropriate prefix based on display mode"""
        return (
            f"{self.pipe_separator}{self.space_separator}"
            if mode == DisplayMode.SAME_LINE
            else self.new_line
        )
