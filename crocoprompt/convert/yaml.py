"""
YAML prompt converter module.
"""

from typing import override

from crocoprompt.construct.base import SectionPrompt
from crocoprompt.convert.base import BaseConverter


class YAMLConverter(BaseConverter):
    """Converter that compiles a SectionPrompt into YAML format.

    It formats each section as a YAML key with a block scalar value (using |).
    """

    @staticmethod
    @override
    def convert(prompt: SectionPrompt, order: list[str] | None = None) -> str:
        """Convert a :class:`~crocoprompt.construct.base.SectionPrompt` to YAML.

        Each section is emitted as a YAML block scalar using the ``|`` literal
        style, with content indented by two spaces.

        Args:
            prompt: The prompt to convert.
            order: Optional section ordering/filtering list.

        Returns:
            A YAML-formatted string with ``key: |\\n  content`` entries
            joined by ``"\\n\\n"``.

        Example:
            >>> from crocoprompt.construct.base import PromptSection, SectionPrompt
            >>> p = SectionPrompt(task=PromptSection(content="Do this."))
            >>> YAMLConverter.convert(p)
            'task: |\\n  Do this.'
        """
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
