"""
Few-shot prompting module.

Provides :class:`FewShotPrompt` for building prompts that include
labelled examples before the main instruction, enabling the model to
learn the expected pattern from demonstrations.
"""

from abc import abstractmethod
from collections import deque

from crocoprompt.construct.base import Example, PromptSection, SectionPrompt


class ABCFewShotPrompt(SectionPrompt):
    """Abstract base class for few-shot prompt strategies.

    Stores examples in a :class:`~collections.deque` and requires
    subclasses to implement :meth:`add_example`.

    Args:
        instructions: The main instruction :class:`~crocoprompt.construct.base.PromptSection`.
    """

    def __init__(self, instructions: PromptSection) -> None:
        super().__init__(instructions=instructions)
        self._examples: deque[Example] = deque()

    @abstractmethod
    def add_example(self, example: Example) -> None:
        """Append an example to the prompt's example pool.

        Args:
            example: The :class:`~crocoprompt.construct.base.Example` to add.

        Raises:
            NotImplementedError: If not overridden by a subclass.
        """
        raise NotImplementedError()


class FewShotPrompt(ABCFewShotPrompt):
    """A concrete few-shot prompt that appends examples before compilation.

    Examples are joined with double newlines and placed under an
    ``"Examples:"`` prefix section during :meth:`compile`.

    Args:
        instructions: The main instruction section.
        examples: An optional pre-populated list of examples.

    Example:
        >>> from crocoprompt.construct.base import Example, PromptSection
        >>> prompt = FewShotPrompt(
        ...     instructions=PromptSection(content="Classify the sentiment."),
        ...     examples=[Example(name="pos", content="Input: great! Output: Positive")],
        ... )
        >>> "Positive" in prompt.compile()
        True
    """

    def __init__(self, instructions: PromptSection, examples: list[Example] | None = None) -> None:
        super().__init__(instructions)
        if examples:
            self._examples.extend(examples)

    def add_example(self, example: Example) -> None:
        """Append a single example to the prompt.

        Args:
            example: The :class:`~crocoprompt.construct.base.Example` to add.
        """
        self._examples.append(example)

    def compile(self, order: list[str] | None = None) -> str:
        """Compile the prompt, inserting all examples as a dedicated section.

        The examples are joined with ``"\\n\\n"`` and added as an
        ``"examples"`` section with an ``"Examples:"`` prefix before
        the sections are compiled.

        Args:
            order: Optional ordering of section names.

        Returns:
            The compiled prompt string.
        """
        self.add_section(
            name="examples",
            section=PromptSection(prefix="Examples:", content="\n\n".join(ex.content for ex in self._examples)),
        )
        if order is None:
            order = self._sections.keys()
        parts = []
        for name in order:
            parts.append(self._sections[name].render())
        return "\n\n".join(parts)
