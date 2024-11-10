"""Base configuration for the generator module"""

from typing import List, Dict
from enum import Enum
from dataclasses import dataclass, field


__all__ = [
    "ColumnType",
    "LatexEnvironment",
    "DisplayMode",
    "TextStyle",
    "StyleConfig",
]


class ColumnType(Enum):
    """Column layout and position types"""

    SINGLE = 1
    LEFT = 1
    RIGHT = 2
    MULTI = 2


@dataclass
class LatexEnvironment:
    """LaTeX environment configuration"""

    begin: str
    end: str

    def wrap(self, content: str) -> List[str]:
        """Wrap content with environment tags"""
        return [self.begin, content, self.end]


class DisplayMode(Enum):
    """Display mode for info text"""

    SAME_LINE = "same_line"
    NEW_LINE = "new_line"


class TextStyle(Enum):
    """Text style enumeration"""

    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"


@dataclass
class StyleConfig:
    """Configuration for text styling"""

    commands: Dict[TextStyle, str] = field(
        default_factory=lambda: {
            TextStyle.BOLD: "\\bfseries",
            TextStyle.ITALIC: "\\itshape",
            TextStyle.UNDERLINE: "\\dotuline",
        }
    )
    href_format: str = "\\href{{{}}}{{{}}}"
    wrapper: str = "{{{}}}"

    def apply_style(self, text: str, style: TextStyle) -> str:
        """Apply single style to text"""
        command = self.commands.get(style)
        return f"{command}{self.wrapper.format(text)}" if command else text

    def wrap_text(self, text: str) -> str:
        """Wrap text in standard wrapper"""
        return self.wrapper.format(text)
