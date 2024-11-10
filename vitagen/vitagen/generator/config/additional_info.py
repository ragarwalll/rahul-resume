"""Configuration for additional info formatting"""

from dataclasses import dataclass

__all = ["AdditionalInfoConfig"]


@dataclass
class AdditionalInfoConfig:
    """Configuration for additional info formatting"""

    command: str = "\\additionalinfo"
    separator: str = " | "
    empty_separator: str = ""

    def get_separator(self, has_both_texts: bool) -> str:
        """Get appropriate separator based on text presence"""
        return self.separator if has_both_texts else self.empty_separator
