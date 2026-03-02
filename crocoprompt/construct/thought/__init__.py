"""
Thought-based prompting strategies (Chain-of-Thought, Chain-of-Knowledge).
"""

from crocoprompt.construct.thought.cok import ChainOfKnowledge, Triplet
from crocoprompt.construct.thought.cot.base import ChainOfThoughtPrompt
from crocoprompt.construct.thought.cot.cue_cot import CueChainOfThoughtPrompt

__all__ = [
    "ChainOfKnowledge",
    "ChainOfThoughtPrompt",
    "CueChainOfThoughtPrompt",
    "Triplet",
]
