"""
Prompt construction strategies for crocoprompt.
"""

from crocoprompt.construct.base import ABCPrompt, Example, PromptSection, SectionPrompt
from crocoprompt.construct.few_shot import ABCFewShotPrompt, FewShotPrompt
from crocoprompt.construct.zero_shot import (
    ZeroShotEmotionPrompt,
    ZeroShotPrompt,
    ZeroShotRolePrompt,
)

__all__ = [
    "ABCFewShotPrompt",
    "ABCPrompt",
    "Example",
    "FewShotPrompt",
    "PromptSection",
    "SectionPrompt",
    "ZeroShotEmotionPrompt",
    "ZeroShotPrompt",
    "ZeroShotRolePrompt",
]
