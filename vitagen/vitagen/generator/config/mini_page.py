"""Configuration for minipage environment"""

from dataclasses import dataclass
from vitagen.generator.config.base import LatexEnvironment

___all__ = ["MinipageConfig"]


@dataclass
class MinipageConfig:
    """Configuration for minipage environment"""

    regular_width: str = "\\dimexpr\\linewidth-2\\fboxsep\\relax"
    full_width: str = "\\textwidth"
    end: str = "\\end{minipage} "

    def get_environment(self, is_full: bool) -> LatexEnvironment:
        """Get appropriate minipage environment"""
        width = self.full_width if is_full else self.regular_width
        return LatexEnvironment(
            begin=f"\\noindent\\begin{{minipage}}{{{width}}}", end=self.end
        )
