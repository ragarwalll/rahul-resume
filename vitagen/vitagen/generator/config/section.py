"""Section configuration generator."""

from dataclasses import dataclass, field
from vitagen.generator.config.base import LatexEnvironment
from vitagen.generator.config.mini_page import MinipageConfig


__all__ = ["SectionConfig"]


@dataclass
class SectionConfig:
    """Configuration for section formatting"""

    minipage: MinipageConfig = field(default_factory=MinipageConfig)
    group: LatexEnvironment = field(
        default_factory=lambda: LatexEnvironment(begin="\\begingroup", end="\\endgroup")
    )
    separator: str = "\\sectionseperator%"
    title_format: str = "\\raggedright\\section{{{}}}"
