"""Inline list configuration module"""

from dataclasses import dataclass


@dataclass
class InlineListConfig:
    """Configuration for inline list formatting"""

    default_separator: str = "\\textbullet{}"
    space_wrapper: str = " "
    new_line: str = "\\newline"
    item_wrapper: str = "{}"

    def wrap_with_space(self, text: str) -> str:
        """Wrap text with configured space wrapper"""
        return f"{self.space_wrapper}{text}{self.space_wrapper}"

    def wrap_item(self, item: str) -> str:
        """Wrap item with configured wrapper"""
        return self.item_wrapper.format(item)
