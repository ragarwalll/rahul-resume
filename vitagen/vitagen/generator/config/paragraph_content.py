"""Configuration for paragraph formatting"""

from dataclasses import dataclass

__all__ = ["ParagraphConfig"]


@dataclass
class ParagraphConfig:
    """Configuration for paragraph formatting"""

    environment: str = "tightnopoints"
    item_command: str = "\\item"
    href_format: str = "\\href{{{}}}{{{}}}"

    def wrap_in_environment(self, content: str) -> str:
        """Wrap content in LaTeX environment"""
        return (
            f"\\begin{{{self.environment}}}"
            f"{self.item_command}{{{content}}}"
            f"\\end{{{self.environment}}}"
        )

    def create_hyperlink(self, text: str, href: str) -> str:
        """Create hyperlink with text"""
        return self.href_format.format(href, text)
