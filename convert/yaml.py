"""
YAML prompt converter module.
"""

from typing import override

from construct.base import SectionPrompt

from convert.base import BaseConverter


class YAMLConverter(BaseConverter):
    """
    Converter that compiles a SectionPrompt into YAML format.
    It formats each section as a YAML key with a block scalar value (using |).
    """

    @staticmethod
    @override
    def convert(prompt: SectionPrompt, order: list[str] | None = None) -> str:
        if order is None:
            order = list(prompt.all_sections())

        parts = []
        for name in order:
            section = prompt.get_section(name)
            content = section.render()

            key = f"{name}:"

            indented_content = "\n".join(f"  {line}" for line in content.splitlines())

            section_content = f"{key} |\n{indented_content}"
            parts.append(section_content)

        return "\n\n".join(parts)
