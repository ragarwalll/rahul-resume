"""
Generate LaTeX resume content from JSON data.
"""

from typing import List, Optional, Dict, Any, Final, Iterator, Callable, Union, Set
from itertools import groupby
from dataclasses import dataclass, field
from operator import itemgetter
import re
from enum import Enum
from functools import lru_cache, reduce


class ColumnType(Enum):
    """Column layout and position types"""

    SINGLE = 1
    LEFT = 1
    RIGHT = 2
    MULTI = 2


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


@dataclass
class LatexEnvironment:
    """LaTeX environment configuration"""

    begin: str
    end: str

    def wrap(self, content: str) -> List[str]:
        """Wrap content with environment tags"""
        return [self.begin, content, self.end]


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


@dataclass
class SectionConfig:
    """Configuration for section formatting"""

    minipage: MinipageConfig = field(default_factory=MinipageConfig)
    group: LatexEnvironment = field(
        default_factory=lambda: LatexEnvironment(begin="\\begingroup", end="\\endgroup")
    )
    separator: str = "\\sectionseperator%"
    title_format: str = "\\raggedright\\section{{{}}}"


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


@dataclass
class SubsectionElements:
    """Configuration for subsection elements"""

    group: tuple[str, str] = ("\\begingroup", "\\endgroup")
    minipage: tuple[str, str] = (
        "\\begin{minipage}[t]{\\columnwidth}",
        "\\end{minipage}",
    )
    heading_format: str = "\\altsubsection{{{}}}"


@dataclass
class MetadataConfig:
    """Configuration for metadata display"""

    location: str = ""
    duration: str = ""
    same_line: bool = False


class DisplayMode(Enum):
    """Display mode for info text"""

    SAME_LINE = "same_line"
    NEW_LINE = "new_line"


@dataclass
class InfoFormatConfig:
    """Configuration for info text formatting"""

    pipe_separator: str = "|"
    space_separator: str = " "
    new_line: str = "\\newline%\n"
    command: str = "\\info"

    def get_prefix(self, mode: DisplayMode) -> str:
        """Get appropriate prefix based on display mode"""
        return (
            f"{self.pipe_separator}{self.space_separator}"
            if mode == DisplayMode.SAME_LINE
            else self.new_line
        )


@dataclass
class AdditionalInfoConfig:
    """Configuration for additional info formatting"""

    command: str = "\\additionalinfo"
    separator: str = " | "
    empty_separator: str = ""

    def get_separator(self, has_both_texts: bool) -> str:
        """Get appropriate separator based on text presence"""
        return self.separator if has_both_texts else self.empty_separator


class ContentType(Enum):
    """Content type enumeration"""

    LIST = "list"
    PARAGRAPH = "paragraph"
    INLINE_LIST = "inline_list"
    TABLE = "table"


@dataclass
class ContentFormatters:
    """Formatters for different content types"""

    list_formatter: Callable[[Dict[str, Any]], str]
    paragraph_formatter: Callable[[Dict[str, Any]], str]
    table_formatter: Callable[[Dict[str, Any]], str]
    inline_list_formatter: Optional[Callable[[Dict[str, Any]], str]] = None

    def get_formatter(self, content_type: str) -> Callable:
        """Get appropriate formatter for content type"""
        formatters = {
            ContentType.LIST.value: self.list_formatter,
            ContentType.PARAGRAPH.value: self.paragraph_formatter,
            ContentType.INLINE_LIST.value: self.inline_list_formatter,
            ContentType.TABLE.value: self.table_formatter or self.list_formatter,
        }
        return formatters.get(content_type, self.list_formatter)


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


@dataclass
class ItemSegment:
    """Structure for list item segments"""

    text: str
    inline_list: Optional[List[str]] = None
    segments: Optional[List[Dict[str, Any]]] = None


@dataclass
class InlineListConfig:
    """Configuration for inline list formatting"""

    default_separator: str = "\\textbullet{}"
    space_wrapper: str = " "
    new_line: str = "\\newline"
    item_wrapper: str = "{}"

    def wrap_with_space(self, text: str) -> str:
        """Wrap text with configured space wrapper"""
        return f"{self.space_wrapper}{text}{self.space_wrapper}"

    def wrap_item(self, item: str) -> str:
        """Wrap item with configured wrapper"""
        return self.item_wrapper.format(item)


class TextStyle(Enum):
    """Text style enumeration"""

    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"


@dataclass
class StyleConfig:
    """Configuration for text styling"""

    commands: Dict[TextStyle, str] = field(
        default_factory=lambda: {
            TextStyle.BOLD: "\\bfseries",
            TextStyle.ITALIC: "\\itshape",
            TextStyle.UNDERLINE: "\\dotuline",
        }
    )
    href_format: str = "\\href{{{}}}{{{}}}"
    wrapper: str = "{{{}}}"

    def apply_style(self, text: str, style: TextStyle) -> str:
        """Apply single style to text"""
        command = self.commands.get(style)
        return f"{command}{self.wrapper.format(text)}" if command else text

    def wrap_text(self, text: str) -> str:
        """Wrap text in standard wrapper"""
        return self.wrapper.format(text)


@dataclass
class TableConfig:
    """Configuration for table formatting"""

    environment: str = "tabular"
    column_format: str = "l"
    row_separator: str = "\n"
    column_separator: str = " & "
    row_end: str = " \\\\"
    begin: str = "\\begin{tabular}{rll}"
    end: str = "\\end{tabular}"

    def wrap_in_environment(self, content: str) -> str:
        """Wrap content in LaTeX environment"""
        return f"{self.begin}%\n{content}%\n{self.end}"

    def format_row(self, cells: List[str], escape_latex: callable) -> str:
        """Format row with cells"""
        cells = [escape_latex(cell) for cell in cells]
        return f"{self.column_separator.join(cells)}{self.row_end}"

    def format_table(self, rows: List[List[str]], escape_latex: callable) -> str:
        """Format table with rows"""
        return self.row_separator.join(
            self.format_row(row, escape_latex) for row in rows
        )


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


class ResumeContentGenerator:
    """Convert JSON data to LaTeX resume content."""

    def __init__(self, json_data: Dict[str, Any]):
        self.data = json_data
        self.space_separator = "\\space"
        self.section_seperator = "\\sectionseperator"
        self.formatters = ContentFormatters(
            list_formatter=self.display_list,
            paragraph_formatter=self.display_paragraph,
            inline_list_formatter=self.display_inline_list,
            table_formatter=self.display_table,
        )

    def escape_latex(
        self, text: str, custom_chars: dict[str, str] | None = None
    ) -> str:
        """
        Escape special LaTeX characters in text with optimized performance.

        Args:
            text (str): Input text to escape
            custom_chars (dict[str, str] | None): Optional custom character mappings

        Returns:
            str: Text with LaTeX special characters escaped

        Examples:
            >>> escape_latex("Hello_world & 100%")
            'Hello\\_world \\& 100\\%'
            >>> escape_latex("Cost: $50", {"$": "USD"})
            'Cost: USD50'
        """
        # Define special characters as a constant
        latex_special_chars: Final[dict[str, str]] = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            # "-": r"\-",
            "{": r"\{",
            "}": r"\}",
            " ": r"{\space}",
            ":": r"\:",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
            "\\": r"\textbackslash{}",  # Added backslash escape
            "|": r"\textbar{}",  # Added vertical bar escape
            "<": r"\textless{}",  # Added less than escape
            ">": r"\textgreater{}",  # Added greater than escape
            "'": r"'",  # Added smart quotes
            "`": r"`",  # Added backtick escape
            '"': r"''",  # Added double quote escape
            "\n": r"\newline ",  # Added newline handling
            "\t": r"\quad ",  # Added tab handling
        }

        @lru_cache(maxsize=1024)
        def _escape_char(char: str) -> str:
            """Cache frequently used character replacements."""
            return escape_chars.get(char, char)

        # Merge custom characters with defaults if provided
        escape_chars = latex_special_chars.copy()
        if custom_chars:
            escape_chars.update(custom_chars)

        # Use regex for bulk replacements of most common patterns
        if len(text) > 1000:  # For longer texts, regex might be faster
            pattern = "|".join(map(re.escape, escape_chars.keys()))
            return re.sub(pattern, lambda m: escape_chars[m.group()], text)

        # For shorter texts, use join with generator expression
        return "".join(_escape_char(c) for c in text)

    def format_output_array(self, output: list[str]) -> str:
        """_summary_

        Args:
            key (str): _description_
            output (list[str]): _description_

        Returns:
            str: _description_
        """
        return "%\n".join(output)

    def wrap_in_space(self, text: str) -> str:
        """_summary_

        Args:
            text (str): _description_

        Returns:
            str: _description_
        """
        return f"{self.space_separator}{{{text}}}{self.space_separator}"

    def get_value(self, key_path: str) -> str:
        """Get value from JSON using dot notation."""
        try:
            current = self.data
            for key in key_path.split("."):
                if "[" in key:  # Handle array indexing
                    base_key, index = key.split("[")
                    index = int(index.rstrip("]"))
                    current = current[base_key][index]
                else:
                    current = current.get(key, "")
            return current if current is not None else ""
        except (KeyError, IndexError, AttributeError):
            return ""

    def process_header_sections(self) -> str:
        """Process header section."""
        output = []

        first_name = self.get_value("firstName")
        middle_name = self.get_value("middleName")
        last_name = self.get_value("lastName")
        links = ""

        # depending on where any or all of the names are missing, the full name is constructed
        # if lets say the first name is missing,
        # the full name will be the middle name and last name
        # with self.space_separator in between
        if middle_name:
            first_name = f"{first_name} {middle_name}"

        if self.data.get("links"):
            links = self.process_links(self.data.get("links", []))

        output.append(
            f"\\namesection{{{first_name}}}{{{last_name}}}{{\\urlstyle{{same}}{links}}}"
        )

        return self.format_output_array(output)

    def process_links(self, links: list[dict[str, str]]) -> str:
        """Process links and generate LaTeX output.

        Args:
            links (list[dict[str, str]]): List of links containing 'href', 'text' and optional 'column'

        Returns:
            str: Formatted LaTeX output with links organized by columns and separated by '|' and '\\'
        """
        if not links:
            return ""

        # Convert links to (column, formatted_link) tuples with default column=1
        formatted_links = [
            (link.get("column", 1), f'\\href{{{link["href"]}}}{{{link["text"]}}}')
            for link in links
        ]

        # Sort by column first for groupby to work correctly
        formatted_links.sort(key=itemgetter(0))

        # Create dictionary of column: joined_links using dict comprehension
        result_by_column = {
            col: " | ".join(link for _, link in group)
            for col, group in groupby(formatted_links, key=itemgetter(0))
        }

        # Build final result with column separators
        max_column = max(result_by_column.keys())
        return self.format_output_array(
            [
                result_by_column.get(col, "") + ("" if col == max_column else "\\\\")
                for col in range(1, max_column + 1)
            ]
        )

    def process_sections(
        self,
        sections: List[Dict],
        process_section: callable,
        golden_ratio: float = 0.618,
    ) -> str:
        """
        Process resume sections for single/multi-column layout.

        Args:
            sections: List of section dictionaries
            process_section: Function to process individual sections
            golden_ratio: Column ratio (default: golden ratio 0.618)

        Returns:
            str: Formatted LaTeX output

        Example:
            >>> sections = [
            ...     {"title": "Education", "column": 1},
            ...     {"title": "Experience", "column": 2}
            ... ]
            >>> result = process_sections(sections, process_single_section)
        """
        if not sections:
            return ""

        def get_column(section: Dict) -> int:
            """Get section column number with default to 1"""
            return section.get("column", ColumnType.SINGLE.value)

        # Check if multi-column layout is needed
        is_multi_column = any(
            get_column(section) == ColumnType.RIGHT.value for section in sections
        )

        # Single column layout processing
        if not is_multi_column:
            return "\n" + "".join(map(process_section, sections))

        # Setup multi-column configuration
        col_config = LatexColumn(ratio=golden_ratio)

        # Group sections by column
        sorted_sections = sorted(sections, key=get_column)
        sections_by_column = {
            col: list(group) for col, group in groupby(sorted_sections, key=get_column)
        }

        # Build multi-column layout
        layout = [
            f"\\columnratio{{{col_config.ratio}}}",
            col_config.begin,
            # Left column
            col_config.left_begin,
            *map(process_section, sections_by_column.get(ColumnType.LEFT.value, [])),
            col_config.left_end,
            # Right column
            col_config.right_begin,
            *map(process_section, sections_by_column.get(ColumnType.RIGHT.value, [])),
            col_config.right_end,
            col_config.end,
        ]

        spacing = SpacingModel[
            self.data.get("spacing", SpacingModel.NORMAL.name).upper()
        ].value
        # Filter out empty strings and join with newlines
        return self.format_output_array(
            LatexScalingFactor().wrap(
                "\n".join(filter(None, layout)),
                spacing,
            )
        )

    def process_single_section(
        self,
        section: Dict[str, Any],
        config: Optional[SectionConfig] = None,
    ) -> str:
        """
        Process a single resume section into LaTeX format.
        """
        if not section:
            return ""

        # Use default config if none provided
        config = config or SectionConfig()

        # Get appropriate minipage environment based on width
        is_full_width = section.get("fullWidth", False)
        minipage_env = config.minipage.get_environment(is_full_width)

        def build_section() -> List[str]:
            """Build section components"""
            components = [
                minipage_env.begin,
                "%",  # LaTeX comment
                "\\sloppy",
                config.group.begin,
                config.separator,
                config.title_format.format(section.get("heading", "")),
            ]

            # Process subsections if available
            if section.get("subsections"):
                components.append(self.process_subsections(section))

            # Add content if available
            if section.get("content"):
                components.append(self.display_content(section.get("content")))

            # Add closing tags
            components.extend([config.group.end, config.separator, minipage_env.end])

            return components

        # Filter out empty strings and join with newlines
        return "\n".join(filter(None, build_section()))

    def process_subsections(
        self,
        section: Dict[str, Any],
        config: Optional[SubsectionConfig] = None,
    ) -> str:
        """
        Process subsections of a section with single/multi-column layout.

        Args:
            section: Section data containing subsections and column settings
            config: Optional subsection configuration

        Returns:
            str: Formatted LaTeX output for subsections

        Example:
            >>> section = {
            ...     "subsections": [
            ...         {"title": "Skills", "items": ["Python", "Java"]},
            ...         {"title": "Languages", "items": ["English", "Spanish"]}
            ...     ],
            ...     "columnSettings": 2
            ... }
            >>> result = process_subsections(section, process_single_subsection)
        """
        # Get subsections or return empty string
        subsections = section.get("subsections", [])
        if not subsections:
            return ""

        # Use default config if none provided
        config = config or SubsectionConfig()

        def process_single_column() -> Iterator[str]:
            """Process subsections in single column layout"""
            return (
                self.process_single_subsection(subsection, with_mini_page=False)
                for subsection in subsections
            )

        def process_multi_column(num_columns: int) -> List[str]:
            """Process subsections in multi-column layout"""
            return [
                config.multicol_sep,
                f"{config.multicol_begin}{{{num_columns}}}",
                *[
                    self.process_single_subsection(subsection, with_mini_page=True)
                    for subsection in subsections
                ],
                config.multicol_end,
            ]

        # Get column settings
        column_count = config.get_column_settings(section)

        # Process based on layout type
        if column_count == ColumnType.SINGLE.value:
            return f"{self.section_seperator}%\n".join(
                filter(None, process_single_column())
            )

        return f"{self.section_seperator}%\n".join(
            filter(None, process_multi_column(column_count))
        )

    def process_single_subsection(
        self,
        subsection: Dict[str, Any],
        with_mini_page: bool = False,
        elements: Optional[SubsectionElements] = None,
    ) -> str:
        """
        Process a single subsection into LaTeX format.

        Args:
            subsection: Subsection data including heading, info, content and metadata
            with_mini_page: Whether to wrap content in minipage environment
            elements: Optional subsection elements configuration

        Returns:
            str: Formatted LaTeX output for subsection

        Example:
            >>> subsection = {
            ...     "heading": "Project X",
            ...     "info": {"title": "Lead Developer", "sameLine": True},
            ...     "metadata": {"location": "New York", "duration": "2020-2021"},
            ...     "content": ["Developed features", "Led team"]
            ... }
            >>> result = process_single_subsection(subsection)
        """
        if not subsection:
            return ""

        elements = elements or SubsectionElements()

        def build_subsection() -> List[str]:
            """Build subsection components"""
            components = [elements.group[0]]  # Begin group

            # Add minipage if requested
            if with_mini_page:
                components.append(elements.minipage[0])

            # Process heading
            if heading := self.escape_latex(subsection.get("heading", "")):
                components.append(elements.heading_format.format(heading))

            # Process info block
            if info := subsection.get("info", {}):
                if title := info.get("title"):
                    components.append(
                        self.display_info(title, same_line=info.get("sameLine", False))
                    )

            # Process metadata
            if metadata := subsection.get("metadata", {}):
                components.append(
                    self.display_additional_info(
                        metadata.get("location", ""), metadata.get("duration", "")
                    )
                )

            # Process content
            if content := subsection.get("content"):
                components.append(self.display_content(content))

            # Close environments
            if with_mini_page:
                components.append(elements.minipage[1])
            components.append(elements.group[1])

            return components

        # Filter out empty strings and join with newlines
        return "\n".join(filter(None, build_subsection()))

    def display_info(
        self,
        text: str,
        same_line: bool = False,
        config: Optional[InfoFormatConfig] = None,
    ) -> str:
        """
        Display info content with configurable formatting.

        Args:
            text: Text content to display
            same_line: If True, adds pipe separator before text
            config: Optional formatting configuration

        Returns:
            str: Formatted LaTeX info command

        Examples:
            >>> display_info("Project Lead")
            '\\newline%\n\\info{{Project Lead}}'

            >>> display_info("Senior Developer", same_line=True)
            '\\info{| {Senior Developer}}'

            >>> custom_config = InfoFormatConfig(pipe_separator="•")
            >>> display_info("Team Lead", same_line=True, config=custom_config)
            '\\info{• {Team Lead}}'
        """
        # Use default config if none provided
        config = config or InfoFormatConfig()

        # Use provided escape function or identity function
        escape_func = self.escape_latex or (lambda x: x)

        def format_info(display_mode: DisplayMode) -> str:
            """Format info text with appropriate prefixes"""
            prefix = config.get_prefix(display_mode)
            escaped_text = escape_func(text)

            return "".join(
                [
                    config.command,
                    "{",  # Open outer brace
                    prefix,
                    "{",  # Open inner brace
                    escaped_text,
                    "}",  # Close inner brace
                    "}",  # Close outer brace
                ]
            )

        # Choose display mode based on same_line parameter
        mode = DisplayMode.SAME_LINE if same_line else DisplayMode.NEW_LINE
        return format_info(mode)

    def display_additional_info(
        self,
        primary_text: str,
        secondary_text: str,
        config: Optional[AdditionalInfoConfig] = None,
    ) -> str:
        """
        Format additional info with primary and secondary text in LaTeX.

        Args:
            primary_text: Main text content
            secondary_text: Supplementary text content
            config: Optional formatting configuration

        Returns:
            str: Formatted LaTeX command

        Examples:
            >>> display_additional_info("New York", "2020-2021")
            '\\additionalinfo{{New York} | {2020-2021}}'

            >>> display_additional_info("Remote", "")
            '\\additionalinfo{{Remote}}'

            >>> config = AdditionalInfoConfig(separator=" • ")
            >>> display_additional_info("San Francisco", "Full-time", config=config)
            '\\additionalinfo{{San Francisco} • {Full-time}}'
        """
        # Use default config if none provided
        config = config or AdditionalInfoConfig()

        # Use provided escape function or identity function
        escape_func = self.escape_latex or (lambda x: x)

        def format_text() -> str:
            """Format text with appropriate separators"""
            # Escape both texts
            escaped_primary = escape_func(primary_text)
            escaped_secondary = escape_func(secondary_text)

            # Get separator based on text presence
            separator = config.get_separator(bool(primary_text and secondary_text))

            # Construct inner content
            inner_content = []
            if primary_text:
                inner_content.append(f"{{{escaped_primary}}}")
            if separator:
                inner_content.append(separator)
            if secondary_text:
                inner_content.append(f"{{{escaped_secondary}}}")

            return "".join(inner_content)

        # Return full command
        return f"{config.command}{{{format_text()}}}"

    def display_content(
        self,
        content: Union[Dict[str, Any], List[str]],
        default_type: str = ContentType.LIST.value,
    ) -> str:
        """
        Display content based on its type with appropriate formatting.

        Args:
            content: Content dictionary with type and data or direct list of items
            default_type: Default content type if not specified

        Returns:
            str: Formatted content using appropriate display methods

        Examples:
            >>> formatters = ContentFormatters(
            ...     list_formatter=lambda x: '\\begin{itemize}\\item ' + '\\item '.join(x['items']) + '\\end{itemize}',
            ...     paragraph_formatter=lambda x: '\\par ' + x['text']
            ... )
            >>> content = {"type": "list", "items": ["Item 1", "Item 2"]}
            >>> print(display_content(content, formatters))
            \\begin{itemize}\\item Item 1\\item Item 2\\end{itemize}
        """
        formatters = self.formatters

        # Handle direct list input
        if isinstance(content, list):
            content = {"type": default_type, "items": content}

        # Handle empty or invalid content
        if not content or not isinstance(content, dict):
            return ""

        def format_content() -> str:
            """Format content using appropriate formatter"""
            content_type = content.get("type", default_type)
            formatter = formatters.get_formatter(content_type)
            return formatter(content)

        return format_content()

    def display_table(
        self, content: Dict[str, Any], config: Optional[TableConfig] = None
    ):
        """
        Display table content with rows and columns.

        Args:
            content: Table content with rows and columns
            config: Optional table formatting configuration

        Returns:
            str: Formatted LaTeX table
        """

        # Use default config if none provided
        config = config or TableConfig()

        def format_table() -> str:
            """Format table with rows and columns"""
            if not (rows := content.get("rows", [])):
                return ""

            # Build table
            return config.wrap_in_environment(
                config.format_table(rows, self.escape_latex)
            )

        return format_table()

    def display_list(
        self,
        content: Dict[str, Any],
        config: Optional[ListFormatConfig] = None,
    ) -> str:
        """
        Display list content with optional bullets and inline lists.

        Args:
            content: List content with items, bullet settings and inline lists
            config: Optional list formatting configuration

        Returns:
            str: Formatted LaTeX list

        Example:
            >>> content = {
            ...     "items": [
            ...         {
            ...             "segments": [{"text": "Lead Developer"}],
            ...             "inlineList": ["Python", "Java"]
            ...         }
            ...     ],
            ...     "style": {"showBullets": True}
            ... }
            >>> result = display_list(content, process_segment, format_inline_list)
        """
        # Use default config if none provided
        config = config or ListFormatConfig()

        def format_segments(segments: List[Dict[str, Any]]) -> str:
            """Format list of segments"""
            processed_segments = [
                f"{{{self.process_single_segment(segment)}}}" for segment in segments
            ]
            return f"\\item{config.space_separator.join(processed_segments)}"

        def process_list_item(item: Dict[str, Any]) -> str:
            """Process single list item with its segments and inline list"""
            # Get environment type
            show_bullets = content.get("style", {}).get("showBullets", True)
            env = config.get_environment(show_bullets)

            components = []

            # Add environment begin
            components.append(f"\\begin{{{env}}}")

            # Add segments if present
            if segments := item.get("segments"):
                components.append(format_segments(segments))

            # Add environment end
            components.append(f"\\end{{{env}}}")

            # Add inline list if present
            if inline_list := item.get("inlineList"):
                components.append(self.display_inline_list(inline_list))
                # components.append("\n")

            return "\n".join(filter(None, components))

        def build_list() -> str:
            """Build complete list with all items"""
            if not (items := content.get("items", [])):
                return ""

            # Process all items
            processed_items = [*[process_list_item(item) for item in items]]

            # check if processed items[0] ends with "\newline"
            # if yes append newline to the end to processed_items[0]
            if processed_items[-1].endswith("inline_list"):
                processed_items[-1] += "\n\\vspace{\\baselineskip}\\\\"

            # Wrap in group
            components = [config.group_begin, *processed_items, config.group_end]

            return "\n".join(filter(None, components))

        return build_list()

    def display_inline_list(
        self, inline_list: Dict[str, Any], config: Optional[InlineListConfig] = None
    ) -> str:
        """
        Display items as inline list with custom separator.

        Args:
            inline_list: Dictionary containing items and separator
            config: Optional formatting configuration

        Returns:
            str: Formatted inline list with wrapped separator

        Examples:
            >>> items = {
            ...     "items": ["Python", "Java", "SQL"],
            ...     "separator": "•"
            ... }
            >>> print(display_inline_list(items))
            {Python} • {Java} • {SQL}
            \\newline

            >>> custom_config = InlineListConfig(default_separator="|")
            >>> print(display_inline_list(items, custom_config))
            {Python} | {Java} | {SQL}
            \\newline
        """
        # Use default config if none provided
        config = config or InlineListConfig()

        def format_list(items: List[str], separator: str) -> str:
            """Format list items with separator"""
            if not items:
                return ""

            # Process items
            wrapped_items = [config.wrap_item(item) for item in items]

            # Get wrapped separator
            wrapped_separator = config.wrap_with_space(separator)

            # Join items with separator
            return wrapped_separator.join(wrapped_items)

        def build_inline_list() -> str:
            """Build complete inline list with newline"""
            # Get items and separator
            items = inline_list.get("items", [])
            separator = inline_list.get("separator", config.default_separator)

            # Format list
            formatted_list = format_list(items, separator)

            # Add newline if content exists
            if formatted_list:
                return f"{formatted_list}%inline_list"

            return ""

        return build_inline_list()

    def process_single_segment(
        self,
        segment: Dict[str, Any],
        config: Optional[StyleConfig] = None,
    ) -> str:
        """
        Process text segment with styling and hyperlink.

        Args:
            segment: Segment data containing text, styles and href
            config: Optional style configuration

        Returns:
            str: LaTeX formatted text with applied styles

        Examples:
            >>> segment = {
            ...     "text": "Important text",
            ...     "style": {"bold": True, "italic": True},
            ...     "href": "https://example.com"
            ... }
            >>> result = process_single_segment(segment, escape_latex)
            >>> print(result)
            {\\bfseries{\\itshape{\\href{https://example.com}{Important text}}}}
        """
        # Use default config if none provided
        config = config or StyleConfig()

        def get_active_styles(style_dict: Dict[str, bool]) -> Set[TextStyle]:
            """Get set of active styles from style dictionary"""
            return {style for style in TextStyle if style_dict.get(style.value, False)}

        def apply_styles(text: str, styles: Set[TextStyle]) -> str:
            """Apply multiple styles to text"""

            def apply_style_chain(t, style):
                return config.apply_style(t, style)

            return reduce(apply_style_chain, styles, text)

        def process_text() -> str:
            """Process text with styles and hyperlink"""
            # Get and escape text
            text = self.escape_latex(segment.get("text", ""))

            # Get active styles
            styles = get_active_styles(segment.get("style", {}))

            # Apply styles
            styled_text = apply_styles(text, styles)

            # Add hyperlink if present
            if href := segment.get("href"):
                styled_text = config.href_format.format(href, styled_text)

            return config.wrap_text(styled_text)

        return process_text()

    def display_paragraph(
        self,
        content: Dict[str, Any],
        config: Optional[ParagraphConfig] = None,
    ) -> str:
        """
        Display paragraph content with optional hyperlink.

        Args:
            content: Paragraph data with text and optional href
            config: Optional paragraph formatting configuration

        Returns:
            str: LaTeX formatted paragraph

        Examples:
            >>> content = {
            ...     "text": "Visit our website",
            ...     "href": "https://example.com"
            ... }
            >>> print(display_paragraph(content))
            \\begin{tightnopoints}\\item{\\href{https://example.com}{Visit our website}}\\end{tightnopoints}

            >>> content = {"text": "Simple paragraph"}
            >>> print(display_paragraph(content))
            \\begin{tightnopoints}\\item{Simple paragraph}\\end{tightnopoints}
        """
        # Use default config if none provided
        config = config or ParagraphConfig()

        # Use provided escape function or identity function
        escape_func = self.escape_latex or (lambda x: x)

        def format_paragraph_text(text: str, href: Optional[str] = None) -> str:
            """Format paragraph text with optional hyperlink"""
            # Escape text if function provided
            escaped_text = escape_func(text)

            # Add hyperlink if present
            if href:
                return config.create_hyperlink(escaped_text, href)

            return escaped_text

        def build_paragraph() -> str:
            """Build complete paragraph with environment"""
            # Get text and href
            text = content.get("text", "")
            href = content.get("href")

            # Format text with hyperlink if present
            formatted_text = format_paragraph_text(text, href)

            # Wrap in environment
            return config.wrap_in_environment(formatted_text)

        return build_paragraph()

    def build_resume(self) -> str:
        """Build resume content."""
        output = ["% chktex-file 6", "% chktex-file 36"]

        output.append("% ============ Display Presets ============")
        preset = self.get_value("preset")
        if preset:
            output.append(f"\\loadpresent{{{preset}}}")
        else:
            output.append("\\loadpresent{deedy-inspired-open-fonts}")

        output.append("% ======== Display Last Updated ==========")
        if self.data.get("showLastUpdated", True):
            output.append("\\lastupdated%")

        # process name section
        output.append("% ============ Display Header ============")
        output.append(self.process_header_sections())

        # process sections
        output.append("% ============ Display Sections ============")
        output.append(
            self.process_sections(
                self.get_value("resume.sections"), self.process_single_section
            )
        )

        return self.format_output_array(output)


def str_to_bool(value):
    """Convert string to boolean."""
    if isinstance(value, bool):
        return value
    return str(value).lower() in ("true", "t", "yes", "y", "1")
