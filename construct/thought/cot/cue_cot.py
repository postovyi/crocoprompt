from construct.base import PromptSection
from construct.thought.cot.base import ChainOfThoughtPrompt


class CueChainOfThoughtPrompt(ChainOfThoughtPrompt):
    def __init__(self, instructions: PromptSection, thinking: PromptSection, cue: PromptSection) -> None:
        super().__init__(instructions=instructions, thinking=thinking)
        self.add_section(name="cue", section=cue)
