"""
Base converter module defining interfaces for compiling prompt modules into string formats.
"""

from abc import ABC, abstractmethod

from crocoprompt.construct.base import SectionPrompt


class BaseConverter(ABC):
    """Abstract base class for prompt converters."""

    @staticmethod
    @abstractmethod
    def convert(prompt: SectionPrompt, order: list[str] | None = None) -> str:
        """
        Convert a SectionPrompt into a specific string format representation.

        Args:
            prompt: The prompt to convert.
            order: Optional order of sections to process.

        Returns:
            The compiled string representation of the prompt in the target format.
        """
        pass
