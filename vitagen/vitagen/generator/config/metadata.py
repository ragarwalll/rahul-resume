"""Configuration for metadata display"""

from dataclasses import dataclass

__all__ = ["MetadataConfig"]


@dataclass
class MetadataConfig:
    """Configuration for metadata display"""

    location: str = ""
    duration: str = ""
    same_line: bool = False
