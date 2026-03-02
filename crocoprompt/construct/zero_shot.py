"""
Zero-shot prompting module.

Provides prompt classes for zero-shot scenarios — where the model receives
only instructions without demonstration examples. Variants include role
conditioning and emotion priming.
"""

from crocoprompt.construct.base import PromptSection, SectionPrompt


class ZeroShotPrompt(SectionPrompt):
    """A basic zero-shot prompt containing only an instructions section.

    Args:
        instructions: The instruction :class:`~crocoprompt.construct.base.PromptSection`.

    Example:
        >>> from crocoprompt.construct.base import PromptSection
        >>> prompt = ZeroShotPrompt(instructions=PromptSection(content="Translate to French."))
        >>> prompt.compile()
        'Translate to French.'
    """

    def __init__(self, instructions: PromptSection) -> None:
        super().__init__(instructions=instructions)


class ZeroShotRolePrompt(ZeroShotPrompt):
    """A zero-shot prompt that prepends a role definition.

    The role section is inserted before the instructions section so
    the model receives persona context first.

    Args:
        instructions: The instruction section.
        role: A plain string describing the model's role (e.g. ``"Expert Translator"``).

    Example:
        >>> prompt = ZeroShotRolePrompt(
        ...     instructions=PromptSection(content="Translate to French."),
        ...     role="Expert Translator",
        ... )
        >>> prompt.compile().startswith("Role:")
        True
    """

    def __init__(self, instructions: PromptSection, role: str) -> None:
        super().__init__(instructions)
        self.role = PromptSection(prefix="Role:", content=role)
        self.add_section(name="role", section=self.role)
        self._sections.move_to_end("role", last=False)


class ZeroShotEmotionPrompt(ZeroShotPrompt):
    """A zero-shot prompt that appends an emotional framing section.

    Emotion prompting adds an affective instruction (e.g. expressing
    urgency or enthusiasm) after the main instructions.

    Args:
        instructions: The instruction section.
        emotion: A plain string describing the emotional tone or motivation.

    Example:
        >>> prompt = ZeroShotEmotionPrompt(
        ...     instructions=PromptSection(content="Summarise this."),
        ...     emotion="This is very important to my career.",
        ... )
        >>> "Emotion:" in prompt.compile()
        True
    """

    def __init__(self, instructions: PromptSection, emotion: str) -> None:
        super().__init__(instructions)
        self.emotion = PromptSection(prefix="Emotion:", content=emotion)
        self.add_section(name="emotion", section=self.emotion)
