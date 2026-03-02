"""
Markdown prompt converter module.
"""

from typing import override

from crocoprompt.construct.base import SectionPrompt
from crocoprompt.convert.base import BaseConverter


class MarkdownConverter(BaseConverter):
    """Converter that compiles a SectionPrompt into Markdown format.

    It uses Markdown headers (#) for section names.
    """

    @staticmethod
    @override
    def convert(prompt: SectionPrompt, order: list[str] | None = None) -> str:
        """Convert a :class:`~crocoprompt.construct.base.SectionPrompt` to Markdown.

        Each section becomes a level-1 Markdown header (``#``) with the
        section name title-cased and underscores replaced by spaces.

        Args:
            prompt: The prompt to convert.
            order: Optional list of section names controlling which sections
                are included and in what order. Defaults to all sections in
                insertion order.

        Returns:
            A Markdown-formatted string with ``# Header\\ncontent`` blocks
            joined by ``"\\n\\n"``.

        Example:
            >>> from crocoprompt.construct.base import PromptSection, SectionPrompt
            >>> p = SectionPrompt(my_task=PromptSection(content="Do this."))
            >>> MarkdownConverter.convert(p)
            '# My Task\\nDo this.'
        """
        if order is None:
            order = list(prompt.all_sections())

        parts = []
        for name in order:
            section = prompt.get_section(name)
            # Convert section name to a title-cased header
            title = name.replace("_", " ").title()

            section_content = f"# {title}\n"
            content = section.render()

            section_content += content
            parts.append(section_content)

        return "\n\n".join(parts)
