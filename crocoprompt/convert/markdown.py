"""
Markdown prompt converter module.
"""

from typing import override

from construct.base import SectionPrompt

from crocoprompt.convert.base import BaseConverter


class MarkdownConverter(BaseConverter):
    """
    Converter that compiles a SectionPrompt into Markdown format.
    It uses Markdown headers (#) for section names.
    """

    @staticmethod
    @override
    def convert(prompt: SectionPrompt, order: list[str] | None = None) -> str:
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
