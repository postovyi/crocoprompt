"""
Chain-of-Knowledge (CoK) prompting module.

Chain-of-Knowledge augments a prompt with structured knowledge triplets
— subject-predicate-object triples — that ground the model's reasoning
in explicit facts before it produces an answer.

Reference:
    Li et al., "Chain of Knowledge: A Framework for Grounding Large Language Models
    with Structured Knowledge Bases", 2023.
"""

from dataclasses import dataclass

from crocoprompt.construct.base import PromptSection
from crocoprompt.construct.zero_shot import ZeroShotPrompt


@dataclass
class Triplet:
    """A knowledge triplet representing a subject-predicate-object fact.

    Triplets are used in :class:`ChainOfKnowledge` to ground the model
    in structured factual knowledge.

    Attributes:
        items: A list of exactly three strings ``[subject, predicate, object]``.

    Example:
        >>> t = Triplet(items=["Paris", "is capital of", "France"])
        >>> str(t)
        "['Paris', 'is capital of', 'France']"
    """

    items: list[str]

    def __str__(self) -> str:
        """Return a string representation of the triplet items list.

        Returns:
            Python's default list ``repr`` of ``self.items``.
        """
        return str(self.items)


class ChainOfKnowledge(ZeroShotPrompt):
    """A prompt that grounds the model using knowledge triplets.

    Composes three sections: ``instructions``, ``knowledge_triplets``,
    and ``explanation``. The triplets section contains all facts joined
    by double newlines.

    Args:
        instructions: The main task instruction section.
        knowledge_triplets: A list of :class:`Triplet` facts to inject.
        explanation: A follow-up section directing the model to use the
            injected knowledge.

    Example:
        >>> from crocoprompt.construct.base import PromptSection
        >>> prompt = ChainOfKnowledge(
        ...     instructions=PromptSection(content="Answer the question."),
        ...     knowledge_triplets=[Triplet(items=["Sky", "is", "blue"])],
        ...     explanation=PromptSection(content="Use the above facts."),
        ... )
        >>> "instructions" in prompt.all_sections()
        True
    """

    def __init__(
        self, instructions: PromptSection, knowledge_triplets: list[Triplet], explanation: PromptSection
    ) -> None:
        super().__init__(instructions)
        self.add_section(
            name="knowledge_triplets",
            section=PromptSection(content="\n\n".join([str(triplet) for triplet in knowledge_triplets])),
        )
        self.add_section(name="explanation", section=explanation)
