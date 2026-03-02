"""
crocoprompt — A prompt engineering toolkit for structured LLM prompt construction
and format conversion.

Quick start::

    from crocoprompt import ZeroShotPrompt, MarkdownConverter
    from crocoprompt.construct.base import PromptSection

    prompt = ZeroShotPrompt(instructions=PromptSection(content="Summarise this text."))
    print(MarkdownConverter.convert(prompt))
"""

from crocoprompt.construct.base import Example, PromptSection, SectionPrompt
from crocoprompt.construct.few_shot import FewShotPrompt
from crocoprompt.construct.thought.cok import ChainOfKnowledge, Triplet
from crocoprompt.construct.thought.cot.base import ChainOfThoughtPrompt
from crocoprompt.construct.thought.cot.cue_cot import CueChainOfThoughtPrompt
from crocoprompt.construct.zero_shot import (
    ZeroShotEmotionPrompt,
    ZeroShotPrompt,
    ZeroShotRolePrompt,
)
from crocoprompt.convert import MarkdownConverter, XMLConverter, YAMLConverter

__all__ = [
    "ChainOfKnowledge",
    "ChainOfThoughtPrompt",
    "CueChainOfThoughtPrompt",
    "Example",
    "FewShotPrompt",
    "MarkdownConverter",
    "PromptSection",
    "SectionPrompt",
    "Triplet",
    "XMLConverter",
    "YAMLConverter",
    "ZeroShotEmotionPrompt",
    "ZeroShotPrompt",
    "ZeroShotRolePrompt",
]
