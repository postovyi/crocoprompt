from abc import abstractmethod
from collections import deque

from construct.base import Example, PromptSection, SectionPrompt


class ABCFewShotPrompt(SectionPrompt):
    def __init__(self, instructions: PromptSection) -> None:
        super().__init__(instructions=instructions)
        self._examples: deque[Example] = deque()

    @abstractmethod
    def add_example(self, example: Example) -> None:
        raise NotImplementedError()


class FewShotPrompt(ABCFewShotPrompt):
    def __init__(self, instructions: PromptSection, examples: list[Example] | None = None) -> None:
        super().__init__(instructions)
        if examples:
            self._examples.extend(examples)

    def add_example(self, example: Example) -> None:
        self._examples.append(example)

    def compile(self, order: list[str] | None = None) -> str:
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
