"""
Tree-of-Thought (ToT) prompting module.

Implements a structured prompt that organizes intermediate reasoning
into a tree of thoughts with explicit branching and evaluation steps.

Reference:
    Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large
    Language Models", 2023. https://arxiv.org/pdf/2305.10601
"""

from dataclasses import dataclass

from crocoprompt.construct.base import PromptSection
from crocoprompt.construct.zero_shot import ZeroShotPrompt


@dataclass
class ThoughtStep:
    """A single thought step within a reasoning branch.

    Attributes:
        content: Natural language description of the thought.
        score: Optional numeric score representing the quality of the
            thought (e.g. heuristic value or model-assigned rating).
    """

    content: str
    score: float | None = None

    def to_line(self) -> str:
        """Render the thought step as a single line."""
        if self.score is None:
            return self.content
        return f"[score={self.score}] {self.content}"


@dataclass
class ThoughtBranch:
    """A branch in the Tree-of-Thought search process.

    Attributes:
        label: Identifier for the branch (e.g. ``"Branch A"``).
        steps: Ordered list of :class:`ThoughtStep` objects describing
            the reasoning along this branch.
    """

    label: str
    steps: list[ThoughtStep]

    def to_block(self) -> str:
        """Render the branch as a multi-line text block."""
        numbered_steps = [f"{idx + 1}. {step.to_line()}" for idx, step in enumerate[ThoughtStep](self.steps)]
        return f"{self.label}:\n" + "\n".join(numbered_steps)


class TreeOfThoughtPrompt(ZeroShotPrompt):
    """A prompt that structures reasoning as a tree of thoughts.

    This prompt composes four sections:

    * ``instructions`` – the main task description
    * ``thinking_guidelines`` – how the model should explore alternatives
    * ``branches`` – multiple candidate reasoning branches
    * ``selection`` – guidance on selecting or aggregating branches

    Args:
        instructions: The primary task instruction section.
        thinking_guidelines: A section explaining how to generate and
            evaluate alternative thoughts (e.g. breadth/depth, scoring).
        branches: A list of :class:`ThoughtBranch` instances that
            describe candidate reasoning paths.
        selection: A section instructing the model how to aggregate or
            select from the branches to produce a final answer.

    Example:
        >>> from crocoprompt.construct.base import PromptSection
        >>> from crocoprompt.construct.thought.cot.tot import ThoughtStep, ThoughtBranch, TreeOfThoughtPrompt
        >>> prompt = TreeOfThoughtPrompt(
        ...     instructions=PromptSection(content="Solve the puzzle."),
        ...     thinking_guidelines=PromptSection(content="Explore multiple solution paths."),
        ...     branches=[
        ...         ThoughtBranch(
        ...             label="Branch A",
        ...             steps=[ThoughtStep(content="Consider approach X.")],
        ...         )
        ...     ],
        ...     selection=PromptSection(content="Choose the best branch and explain why."),
        ... )
        >>> "branches" in prompt.all_sections()
        True
    """

    def __init__(
        self,
        instructions: PromptSection,
        thinking_guidelines: PromptSection,
        branches: list[ThoughtBranch],
        selection: PromptSection,
    ) -> None:
        super().__init__(instructions=instructions)
        self.add_section(name="thinking_guidelines", section=thinking_guidelines)
        self.add_section(
            name="branches",
            section=PromptSection(content="\n\n".join(branch.to_block() for branch in branches)),
        )
        self.add_section(name="selection", section=selection)
