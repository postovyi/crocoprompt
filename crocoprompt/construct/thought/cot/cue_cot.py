"""
Cue-based Chain-of-Thought (Cue-CoT) prompting module.

Extends the standard Chain-of-Thought with a ``cue`` section that
provides a partial answer scaffold, nudging the model to continue from
a specific starting point (e.g. ``"First, let's consider..."``).
"""

from crocoprompt.construct.base import PromptSection
from crocoprompt.construct.thought.cot.base import ChainOfThoughtPrompt


class CueChainOfThoughtPrompt(ChainOfThoughtPrompt):
    """A Chain-of-Thought prompt augmented with a starting cue.

    The cue section is appended after the thinking section to provide
    a partial reasoning scaffold that the model continues from.

    Args:
        instructions: The main task instruction section.
        thinking: The reasoning framing section.
        cue: A partial statement that seeds the model's response
            (e.g. ``PromptSection(content="First, I notice that")``).

    Example:
        >>> from crocoprompt.construct.base import PromptSection
        >>> prompt = CueChainOfThoughtPrompt(
        ...     instructions=PromptSection(content="Solve this."),
        ...     thinking=PromptSection(content="Let's think step by step."),
        ...     cue=PromptSection(content="First,"),
        ... )
        >>> "cue" in prompt.all_sections()
        True
    """

    def __init__(self, instructions: PromptSection, thinking: PromptSection, cue: PromptSection) -> None:
        super().__init__(instructions=instructions, thinking=thinking)
        self.add_section(name="cue", section=cue)
