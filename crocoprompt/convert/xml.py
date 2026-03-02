"""
XML prompt converter module.
"""

from typing import override

from crocoprompt.construct.base import SectionPrompt
from crocoprompt.convert.base import BaseConverter


class XMLConverter(BaseConverter):
    """Converter that compiles a SectionPrompt into XML format.

    It encloses each section within XML tags matching the section name.
    """

    @staticmethod
    @override
    def convert(prompt: SectionPrompt, order: list[str] | None = None) -> str:
        """Convert a :class:`~crocoprompt.construct.base.SectionPrompt` to XML.

        Each section is wrapped in an XML element whose tag name matches the
        section name (spaces replaced with underscores).

        Args:
            prompt: The prompt to convert.
            order: Optional section ordering/filtering list.

        Returns:
            An XML-formatted string with ``<tag>\\ncontent\\n</tag>`` blocks
            joined by ``"\\n\\n"``.

        Example:
            >>> from crocoprompt.construct.base import PromptSection, SectionPrompt
            >>> p = SectionPrompt(task=PromptSection(content="Do this."))
            >>> XMLConverter.convert(p)
            '<task>\\nDo this.\\n</task>'
        """
        if order is None:
            order = list(prompt.all_sections())

        parts = []
        for name in order:
            section = prompt.get_section(name)
            # Tag names shouldn't have spaces, replacing with underscores just in case
            tag_name = name.replace(" ", "_")
            content = section.render()

            section_content = f"<{tag_name}>\n{content}\n</{tag_name}>"
            parts.append(section_content)

        return "\n\n".join(parts)
