from construct.base import PromptSection
from construct.zero_shot import ZeroShotPrompt


class ChainOfThoughtPrompt(ZeroShotPrompt):
    def __init__(self, instructions: PromptSection, thinking: PromptSection) -> None:
        super().__init__(instructions=instructions)
        self.add_section(name="thinking", section=thinking)
