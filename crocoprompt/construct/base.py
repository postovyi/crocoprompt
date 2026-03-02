"""
Base module with abstract classes for prompt construction.

This module defines the core data structures and abstract base classes
used throughout crocoprompt to represent, compose, and compile prompts.
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, override


@dataclass
class PromptSection:
    """A single section of a prompt with optional variable substitution and wrapping.

    A ``PromptSection`` holds raw content text and supports optional
    prefix/suffix wrapping and ``str.format``-style variable substitution
    via the ``variables`` mapping.

    Attributes:
        content: The main body text of the section. Supports ``{}``-style
            format placeholders when used with ``variables`` or ``format()``.
        variables: An optional mapping of placeholder names to values.
            When set, ``render()`` substitutes them into ``content``.
        prefix: Optional text prepended to the content (separated by a newline).
        suffix: Optional text appended to the content (separated by a newline).

    Example:
        >>> section = PromptSection(
        ...     content="Hello {name}",
        ...     variables={"name": "World"},
        ...     prefix="Greeting:",
        ... )
        >>> section.render()
        'Greeting:\\nHello World'
    """

    content: str
    variables: dict[str, Any] | None = None
    prefix: str | None = None
    suffix: str | None = None

    def render(self) -> str:
        """Render the section to a plain string, applying variables and wrapping.

        Performs variable substitution (if ``variables`` is set) and then
        prepends/appends ``prefix`` and ``suffix`` (each separated by a newline).

        Returns:
            The fully rendered section content as a string.

        Example:
            >>> PromptSection(content="Hi {x}", variables={"x": "there"}).render()
            'Hi there'
        """
        content = self.content
        if self.variables:
            content = self.content.format(**self.variables)
        if self.prefix:
            content = self.prefix + "\n" + content
        if self.suffix:
            content = content + "\n" + self.suffix
        return content

    def format(self, *args: Any, **kwargs: Any) -> str:
        """Apply positional and keyword format arguments to the raw content string.

        Unlike ``render()``, this bypasses ``prefix``, ``suffix``, and
        ``self.variables`` and calls ``str.format`` directly on ``content``.

        Args:
            *args: Positional arguments forwarded to ``str.format``.
            **kwargs: Keyword arguments forwarded to ``str.format``.

        Returns:
            The formatted content string.

        Example:
            >>> PromptSection(content="Hello {} and {name}").format("Alice", name="Bob")
            'Hello Alice and Bob'
        """
        return self.content.format(*args, **kwargs)

    def __str__(self) -> str:
        """Return the content with prefix/suffix applied but without variable substitution.

        Returns:
            The content string wrapped by ``prefix`` and ``suffix`` if set.
        """
        content = self.content
        if self.prefix:
            content = self.prefix + "\n" + content
        if self.suffix:
            content = content + "\n" + self.suffix
        return content


@dataclass
class Example:
    """A named example used in few-shot prompting.

    Attributes:
        name: A short label identifying the example (e.g. ``"Positive"``).
        content: The example body text shown to the model.

    Example:
        >>> ex = Example(name="Positive", content="Input: I love it! Output: Positive")
        >>> ex.content
        'Input: I love it! Output: Positive'
    """

    name: str
    content: str


class ABCPrompt(ABC):
    """Abstract base class for all prompt types.

    Subclasses must implement :meth:`compile`, which converts the prompt
    into a single string ready to be sent to a language model.
    """

    @abstractmethod
    def compile(self, order: list[str] | None = None) -> str:
        """Compile the prompt into a single string.

        Args:
            order: Optional list of section names specifying the order in
                which sections should appear in the output. When ``None``,
                the default insertion order is used.

        Returns:
            The compiled prompt as a plain string.

        Raises:
            NotImplementedError: If not overridden by a subclass.
        """
        raise NotImplementedError()

    @override
    def __str__(self) -> str:
        """Return the compiled prompt as a string (calls :meth:`compile`).

        Returns:
            The output of ``self.compile()`` with no arguments.
        """
        return self.compile()


class SectionPrompt(ABCPrompt):
    """A prompt composed of named :class:`PromptSection` objects.

    Sections are stored in insertion order and compiled by joining their
    rendered content with a double newline separator.

    Args:
        **kwargs: Keyword arguments where each key is a section name and
            each value is a :class:`PromptSection` instance.

    Example:
        >>> prompt = SectionPrompt(
        ...     role=PromptSection(content="You are a helpful assistant."),
        ...     task=PromptSection(content="Summarise the following text."),
        ... )
        >>> print(prompt.compile())
        You are a helpful assistant.
        <BLANKLINE>
        Summarise the following text.
    """

    def __init__(self, **kwargs: Any) -> None:
        self._sections: OrderedDict[str, PromptSection] = OrderedDict(**kwargs)

    def compile(self, order: list[str] | None = None) -> str:
        """Compile all sections into a single string separated by blank lines.

        Args:
            order: Optional list of section names controlling output order.
                Only sections listed here will be included. When ``None``,
                all sections are included in insertion order.

        Returns:
            All rendered sections joined by ``"\\n\\n"``.

        Example:
            >>> prompt = SectionPrompt(a=PromptSection(content="A"), b=PromptSection(content="B"))
            >>> prompt.compile(order=["b", "a"])
            'B\\n\\nA'
        """
        if order is None:
            order = list(self._sections.keys())
        return "\n\n".join(self._sections[name].render() for name in order)

    def add_section(self, name: str, section: PromptSection) -> None:
        """Add or replace a named section in the prompt.

        Args:
            name: The section key used for ordering and retrieval.
            section: The :class:`PromptSection` to store.
        """
        self._sections[name] = section

    def get_section(self, name: str) -> PromptSection:
        """Retrieve a section by name.

        Args:
            name: The section key.

        Returns:
            The :class:`PromptSection` stored under ``name``.

        Raises:
            KeyError: If no section with the given name exists.
        """
        return self._sections[name]

    def all_sections(self) -> OrderedDict[str, PromptSection]:
        """Return the ordered mapping of all sections.

        Returns:
            An :class:`~collections.OrderedDict` mapping section names to
            their :class:`PromptSection` instances, in insertion order.
        """
        return self._sections
