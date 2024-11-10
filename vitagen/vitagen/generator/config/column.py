"""Resume Column Configurations"""

from dataclasses import dataclass

__all__ = ["LatexColumn"]


@dataclass
class LatexColumn:
    """Data class for LaTeX column configuration"""

    ratio: float = 0.618  # Golden ratio
    begin: str = "\\begin{paracol}{2}"
    end: str = "\\end{paracol}"
    left_begin: str = "\\begin{leftcolumn}"
    left_end: str = "\\end{leftcolumn}"
    right_begin: str = "\\begin{rightcolumn}"
    right_end: str = "\\end{rightcolumn}"
