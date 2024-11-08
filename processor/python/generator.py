"""
Generate LaTeX resume content from JSON data.
"""

from typing import Dict, Any


class ResumeContentGenerator:
    """Convert JSON data to LaTeX resume content."""

    def __init__(self, json_data: Dict[str, Any]):
        self.data = json_data
        self.space_separator = "\\space"

    def escape_latex(self, text: str) -> str:
        """
        Escape special LaTeX characters in text.

        Args:
            text (str): Input text to escape

        Returns:
            str: Text with LaTeX special characters escaped
        """
        special_chars = {
            "&": "\\&",
            "%": "\\%",
            "$": "\\$",
            "#": "\\#",
            "_": "\\_",
            "-": "\\-",
            "{": "\\{",
            "}": "\\}",
            ":": "\\:",
            "~": "\\textasciitilde{}",
            "^": "\\textasciicircum{}",
        }
        return "".join(special_chars.get(c, c) for c in text)

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

    def process_name_section(self) -> str:
        """Process name section."""
        output = []

        first_name = self.get_value("firstName")
        middle_name = self.get_value("middleName")
        last_name = self.get_value("lastName")

        # depending on where any or all of the names are missing, the full name is constructed
        # if lets say the first name is missing,
        # the full name will be the middle name and last name
        # with self.space_separator in between
        if middle_name:
            first_name = f"{first_name} {middle_name}"

        output.append(
            f"\\namesection{{{first_name}}}{{{last_name}}}{{\\urlstyle{{same}}}}"
        )

        return self.format_output_array(output)

    def process_sections(self):
        """Process resume sections and generate LaTeX output for single/multi-column layout"""
        sections = self.data.get("resume", {}).get("sections", [])

        # Early return for empty sections
        if not sections:
            return ""

        output = []
        has_multi_column = any(section.get("column", 1) > 1 for section in sections)

        if not has_multi_column:
            # Single column layout - process all sections sequentially
            return (self.process_single_section(section) for section in sections)

        # Multi-column layout with golden ratio (0.618) split
        output.extend(
            ["\\columnratio{0.618}", "\\begin{paracol}{2}", "\\begin{leftcolumn}"]
        )

        # Left column - sections with no column specified or column=1
        output.extend(
            self.process_single_section(section)
            for section in sections
            if not section.get("column") or section.get("column") == 1
        )

        # Right column - sections with column=2
        output.extend(["\\end{leftcolumn}", "\\begin{rightcolumn}"])
        output.extend(
            self.process_single_section(section)
            for section in sections
            if section.get("column") == 2
        )

        output.extend(["\\end{rightcolumn}", "\\end{paracol}"])

        return self.format_output_array(output)

    def process_single_section(self, section: Dict[str, Any]) -> str:
        """
        Process a single resume section into LaTeX format.

        Args:
            section (dict): Section data containing heading, content and subsections

        Returns:
            list: Array of LaTeX commands for the section
        """
        if not section:
            return ""

        output = []

        output.extend(
            [
                "\\noindent\\begin{minipage}{\\dimexpr\\linewidth-2\\fboxsep\\relax}",
                "%",
                "\\sloppy",
                "\\begingroup",
                # Section title
                "\\sectionseperator",
                f"\\raggedright\\section{{{section.get('heading', '')}}}",
            ]
        )

        # Process subsections
        if section.get("subsections"):
            output.append(self.process_subsection(section))

        if section.get("content"):
            output.append(self.display_content(section.get("content")))

        output.extend(["\\endgroup", "\\sectionseperator", "\\end{minipage} "])
        # output.extend(["\\endgroup", "\\end{minipage}"])

        return self.format_output_array(output)

    def process_subsection(self, section: Dict[str, Any]) -> str:
        """
        Process subsections of a section with single/multi-column layout.

        Args:
            section (Dict[str, Any]): Section data containing subsections and column settings

        Returns:
            str: Formatted LaTeX output for subsections
        """
        subsections = section.get("subsections", [])

        # Early return if no subsections
        if not subsections:
            return ""

        # Single column layout (default)
        if section.get("columnSettings", 1) == 1:
            return self.format_output_array(
                self.process_single_sub_section(subsection, with_mini_page=False)
                for subsection in subsections
            )

        # Multi-column layout
        return self.format_output_array(
            [
                "\\setlength{\\multicolsep}{0pt}%",
                f"\\begin{{multicols}}{{{section.get('columnSettings')}}}",
                *[
                    self.process_single_sub_section(subsection, with_mini_page=True)
                    for subsection in subsections
                ],
                f"\\end{{multicols}}",
            ]
        )

    def process_single_sub_section(
        self, subsection: Dict[str, Any], with_mini_page: bool = False
    ) -> str:
        """
        Process a single subsection into LaTeX format.

        Args:
            subsection (Dict[str, Any]): Subsection data including heading, info, content and metadata
            with_mini_page (bool): Whether to wrap content in minipage environment

        Returns:
            str: Formatted LaTeX output for subsection
        """
        if not subsection:
            return ""

        output = ["\\begingroup"]

        if with_mini_page:
            output.append("\\begin{minipage}[t]{\\columnwidth}")

        # Process heading if present
        if heading := self.escape_latex(subsection.get("heading", "")):
            output.append(f"\\altsubsection{{{heading}}}")

        # Process info block
        if info := subsection.get("info", {}):
            if title := info.get("title"):
                output.append(
                    self.display_info(title, same_line=info.get("sameLine", False))
                )

        # Process metadata (duration and location)
        if metadata := subsection.get("metadata", {}):
            output.append(
                self.display_additional_info(
                    metadata.get("location", ""), metadata.get("duration", "")
                )
            )
        # Process main content
        if content := subsection.get("content"):
            output.append(self.display_content(content))

        # Close environments
        if with_mini_page:
            output.append("\\end{minipage}")
        output.append("\\endgroup")

        return self.format_output_array(output)

    def display_info(self, text: str, same_line: bool = False) -> str:
        """
        Display info content with optional spacing for same line display.

        Args:
            text (str): Text content to display
            same_line (bool): If True, adds pipe separator before text

        Returns:
            str: Formatted LaTeX info command with escaped text
        """
        prefix_initial = ""
        prefix_info = ""
        if same_line:
            prefix_info = "|" + self.space_separator
        else:
            prefix_initial = "\\newline%\n"

        return (
            f"{prefix_initial}"
            f"\\info{{"
            f"{prefix_info}"
            f"{{{self.escape_latex(text)}}}"
            f"}}"
        )

    def display_additional_info(self, primary_text: str, secondary_text: str) -> str:
        """
        Format additional info with primary and secondary text in LaTeX.

        Args:
            primary_text (str): Main text content
            secondary_text (str): Supplementary text content

        Returns:
            str: LaTeX command with formatted text and separator
        """
        separator = (
            f"{self.space_separator}|{self.space_separator}"
            if primary_text and secondary_text
            else ""
        )

        return f"\\additionalinfo{{{{{self.escape_latex(primary_text)}}}{separator}{{{self.escape_latex(secondary_text)}}}}}"

    def display_content(self, content: Dict[str, Any]) -> str:
        """
        Display content based on its type (list or paragraph) with optional inline list.

        Args:
            content (Dict[str, Any]): Content with type, data and optional inline list

        Returns:
            str: Formatted content using appropriate display methods
        """
        content_handlers = {
            "list": self.display_list,
            "paragraph": self.display_paragraph,
        }

        output = [
            content_handlers.get(content.get("type", "list"), self.display_list)(
                content
            )
        ]

        return self.format_output_array(output)

    def display_list(self, content: Dict[str, Any]) -> str:
        """
        Display list content with optional bullets and inline lists.

        Args:
            content (Dict[str, Any]): List content with items, bullet settings and inline lists

        Returns:
            str: Formatted LaTeX list with segments and inline content
        """
        if not (items := content.get("items", [])):
            return ""

        show_bullet = str_to_bool(content.get("style", {}).get("showBullets", True))
        environment = "tightemize" if show_bullet else "tightnopoints"

        # Process each item with its segments and inline list
        item_outputs = []
        for item in items:
            # Format segments if present
            segments = (
                f"\\item{self.space_separator.join([f'{{{self.process_single_segment(segment)}}}' for segment in item.get('segments', [])])}"
                if item.get("segments")
                else ""
            )

            # Build item's output with environment and optional inline list
            item_outputs.append(
                self.format_output_array(
                    [
                        f"\\begin{{{environment}}}",
                        segments,
                        f"\\end{{{environment}}}",
                        (
                            self.display_inline_list(item["inlineList"])
                            if item.get("inlineList")
                            else ""
                        ),
                    ]
                )
            )

        # Wrap all items in group
        return self.format_output_array(
            ["{\\setstretch{1}", "\\begingroup", *item_outputs, "\\endgroup}"]
        )

    def display_inline_list(self, inline_list: Dict[str, Any]) -> str:
        """
        Display items as inline list with custom separator.

        Args:
            inline_list (Dict[str, Any]): List data with items and separator

        Returns:
            str: Items joined with wrapped separator
        """
        output = [
            self.wrap_in_space(inline_list.get("seperator", "\\textbullet{}")).join(
                [f"{{{item}}}" for item in inline_list.get("items", [])]
            )
        ]

        if len(output) > 0:
            output.append("\\newline")

        return self.format_output_array(output)

    def process_single_segment(self, segment: Dict[str, Any]) -> str:
        """
        Process text segment with styling and hyperlink.

        Args:
            segment (Dict[str, Any]): Segment data containing text, styles and href

        Returns:
            str: LaTeX formatted text with applied styles
        """
        text = self.escape_latex(segment.get("text", ""))

        style_commands = {
            "bold": "\\bfseries",
            "italic": "\\itshape",
            "underline": "\\dotuline",
        }

        # Apply text styles
        for style, command in style_commands.items():
            if segment.get("style", {}).get(style, False):
                text = f"{command}{{{text}}}"

        # Add hyperlink if present
        if href := segment.get("href"):
            text = f"\\href{{{href}}}{{{text}}}"

        return f"{{{text}}}"

    def display_paragraph(self, content: Dict[str, Any]) -> str:
        """
        Display paragraph content with optional hyperlink.

        Args:
            content (Dict[str, Any]): Paragraph data with text and optional href

        Returns:
            str: LaTeX formatted paragraph in tightnopoints environment
        """
        text = content.get("text", "")

        if href := content.get("href"):
            text = f"\\href{{{href}}}{{{text}}}"

        return f"\\begin{{tightnopoints}}\\item{{{text}}}\\end{{tightnopoints}}"

    def build_resume(self) -> str:
        """Build resume content."""
        output = ["% chktex-file 6"]

        # process name section
        output.append("% ============ Display Header ============")
        output.append(self.process_name_section())

        # process sections
        output.append("% ============ Display Sections ============")
        output.append(self.process_sections())

        return self.format_output_array(output)


def str_to_bool(value):
    """Convert string to boolean."""
    if isinstance(value, bool):
        return value
    return str(value).lower() in ("true", "t", "yes", "y", "1")
