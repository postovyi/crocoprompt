"""
Chain-of-Thought (CoT) prompting variants.
"""

from crocoprompt.construct.thought.cot.base import ChainOfThoughtPrompt
from crocoprompt.construct.thought.cot.cue_cot import CueChainOfThoughtPrompt

__all__ = [
    "ChainOfThoughtPrompt",
    "CueChainOfThoughtPrompt",
]
