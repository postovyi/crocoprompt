"""
Base module with abstract classes for prompt construction.
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, override


@dataclass
class PromptSection:
    content: str
    variables: dict[str, Any] | None = None
    prefix: str | None = None
    suffix: str | None = None

    def render(self) -> str:
        content = self.content.format(**self.variables)
        if self.prefix:
            content = self.prefix + "\n" + content
        if self.suffix:
            content = content + "\n" + self.suffix
        return content

    def format(self, *args: Any, **kwargs: Any) -> str:
        return self.content.format(*args, **kwargs)

    def __str__(self) -> str:
        content = self.content
        if self.prefix:
            content = self.prefix + "\n" + content
        if self.suffix:
            content = content + "\n" + self.suffix
        return content


@dataclass
class Example:
    name: str
    content: str


class ABCPrompt(ABC):
    @abstractmethod
    def compile(self, order: list[str] | None = None) -> str:
        raise NotImplementedError()

    @override
    def __str__(self) -> str:
        return self.compile()


class SectionPrompt(ABCPrompt):
    def __init__(self, **kwargs: Any) -> None:
        self._sections: OrderedDict[str, PromptSection] = OrderedDict(**kwargs)

    def compile(self, order: list[str] | None = None) -> str:
        if order is None:
            order = list(self._sections.keys())
        return "\n\n".join(self._sections[name].render() for name in order)

    def add_section(self, name: str, section: PromptSection) -> None:
        self._sections[name] = section

    def get_section(self, name: str) -> PromptSection:
        return self._sections[name]

    def all_sections(self) -> OrderedDict[str, PromptSection]:
        return self._sections
