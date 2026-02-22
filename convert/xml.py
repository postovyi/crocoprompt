"""
XML prompt converter module.
"""

from typing import override

from construct.base import SectionPrompt

from convert.base import BaseConverter


class XMLConverter(BaseConverter):
    """
    Converter that compiles a SectionPrompt into XML format.
    It encloses each section within XML tags matching the section name.
    """

    @staticmethod
    @override
    def convert(prompt: SectionPrompt, order: list[str] | None = None) -> str:
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
