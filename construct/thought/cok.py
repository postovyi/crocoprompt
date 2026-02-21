from dataclasses import dataclass

from construct.base import PromptSection
from construct.zero_shot import ZeroShotPrompt


@dataclass
class Triplet:
    items: list[str]

    def __str__(self) -> str:
        return str(self.items)


class ChainOfKnowledge(ZeroShotPrompt):
    def __init__(
        self, instructions: PromptSection, knowledge_triplets: list[Triplet], explanation: PromptSection
    ) -> None:
        super().__init__(instructions)
        self.add_section(
            name="knowledge_triplets",
            section=PromptSection(content="\n\n".join([str(triplet) for triplet in knowledge_triplets])),
        )
        self.add_section(name="explanation", section=explanation)
