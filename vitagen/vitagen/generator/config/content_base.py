"""Content base module"""

from enum import Enum
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional
from structlog import BoundLogger

__all__ = ["ContentType", "ContentFormatters"]


class ContentType(Enum):
    """Content type enumeration"""

    LIST = "list"
    PARAGRAPH = "paragraph"
    INLINE_LIST = "inline_list"
    TABLE = "table"


@dataclass
class ContentFormatters:
    """Formatters for different content types"""

    list_formatter: Callable[[Dict[str, Any], BoundLogger], str]
    paragraph_formatter: Callable[[Dict[str, Any], BoundLogger], str]
    table_formatter: Callable[[Dict[str, Any], BoundLogger], str]
    inline_list_formatter: Optional[Callable[[Dict[str, Any], BoundLogger], str]] = None

    def get_formatter(self, content_type: str) -> Callable:
        """Get appropriate formatter for content type"""
        formatters = {
            ContentType.LIST.value: self.list_formatter,
            ContentType.PARAGRAPH.value: self.paragraph_formatter,
            ContentType.INLINE_LIST.value: self.inline_list_formatter,
            ContentType.TABLE.value: self.table_formatter or self.list_formatter,
        }
        return formatters.get(content_type, self.list_formatter)
