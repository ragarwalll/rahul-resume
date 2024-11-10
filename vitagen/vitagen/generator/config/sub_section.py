"""Sub section configuration."""

from dataclasses import dataclass
from typing import Any, Dict

__all__ = ["SubsectionConfig", "SubsectionElements"]


@dataclass
class SubsectionConfig:
    """Configuration for subsection formatting"""

    multicol_sep: str = (
        "\\setlength{\\multicolsep}{\\dimexpr\\fpeval{-10 + (2 * \\spacingscale)}pt\\relax}%"
    )
    multicol_begin: str = "\\begin{multicols}"
    multicol_end: str = "\\end{multicols}"
    default_columns: int = 1

    def get_column_settings(self, section: Dict[str, Any]) -> int:
        """Get column settings with default"""
        return section.get("columnSettings", self.default_columns)


@dataclass
class SubsectionElements:
    """Configuration for subsection elements"""

    group: tuple[str, str] = ("\\begingroup", "\\endgroup")
    minipage: tuple[str, str] = (
        "\\begin{minipage}[t]{\\columnwidth}",
        "\\end{minipage}",
    )
    heading_format: str = "\\altsubsection{{{}}}"
