"""
Chain-of-Thought (CoT) base prompting module.

Provides the base class for chain-of-thought prompts, which include an
explicit reasoning section alongside the main instructions to encourage
the model to think step by step before answering.

Reference:
    Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large
    Language Models", NeurIPS 2022.
"""

from crocoprompt.construct.base import PromptSection
from crocoprompt.construct.zero_shot import ZeroShotPrompt


class ChainOfThoughtPrompt(ZeroShotPrompt):
    """A prompt with an explicit step-by-step thinking section.

    Adds a ``thinking`` section after ``instructions`` to guide the
    model through intermediate reasoning before producing a final answer.

    Args:
        instructions: The task instruction section.
        thinking: A section that frames how the model should reason
            (e.g. ``PromptSection(content="Let's think step by step.")``).

    Example:
        >>> from crocoprompt.construct.base import PromptSection
        >>> prompt = ChainOfThoughtPrompt(
        ...     instructions=PromptSection(content="What is 7 * 8?"),
        ...     thinking=PromptSection(content="Let's think step by step."),
        ... )
        >>> "thinking" in prompt.all_sections()
        True
    """

    def __init__(self, instructions: PromptSection, thinking: PromptSection) -> None:
        super().__init__(instructions=instructions)
        self.add_section(name="thinking", section=thinking)
