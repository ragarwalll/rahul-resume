"""List content configuration."""

from enum import Enum
from dataclasses import dataclass

__all__ = ["ListStyle", "ListFormatConfig"]


class ListStyle(Enum):
    """List style enumeration"""

    BULLET = "tightemize"
    NO_BULLET = "tightnopoints"


@dataclass
class ListFormatConfig:
    """Configuration for list formatting"""

    bullet_env: str = ListStyle.BULLET.value
    no_bullet_env: str = ListStyle.NO_BULLET.value
    space_separator: str = " "
    group_begin: str = "{\\begingroup"
    group_end: str = "\\endgroup}"

    def get_environment(self, show_bullets: bool) -> str:
        """Get appropriate list environment"""
        return self.bullet_env if show_bullets else self.no_bullet_env
