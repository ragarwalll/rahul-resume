"""Spacing factor configuration."""

from enum import Enum
from dataclasses import dataclass
from typing import List

__all__ = ["SpacingModel", "LatexScalingFactor"]


class SpacingModel(Enum):
    """Display sizing mode for LaTeX content"""

    TIGHT = 0.7  # Tight spacing
    ULTRA = 0.78  # Ultimate density
    MAXIMUM = 0.81  # Maximum practical density
    HIGH_DENSE = 0.84  # High content density
    PRO_DENSE = 0.87  # Professional density
    SEMI_DENSE = 0.9  # Moderately dense
    LIGHT_DENSE = 0.95  # Slightly increased density
    COMPACT = 0.85  # Dense, maximizes space
    NORMAL = 1.0  # Standard spacing
    COZY = 1.15  # Comfortable reading
    AIRY = 1.3  # Lots of whitespace
    MINIMAL = 0.75  # Ultra-compact
    SPACIOUS = 1.4  # Maximum readability


@dataclass
class LatexScalingFactor:
    """Data class for LaTeX scaling modifier configuration"""

    begin: str = "\\begin{scalingfactor}{spacing_here}\n\\begingroup"
    end: str = "\\endgroup\n\\end{scalingfactor}"

    def wrap(self, content: str, spacing: int) -> List[str]:
        """Wrap content with size modifier tags"""

        return [self.begin.replace("spacing_here", str(spacing)), content, self.end]
