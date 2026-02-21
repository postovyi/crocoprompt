"""
Module with techniques for Zero-shot prompting.
"""

from construct.base import PromptSection, SectionPrompt


class ZeroShotPrompt(SectionPrompt):
    def __init__(self, instructions: PromptSection) -> None:
        super().__init__(instructions=instructions)


class ZeroShotRolePrompt(ZeroShotPrompt):
    def __init__(self, instructions: PromptSection, role: str) -> None:
        super().__init__(instructions)
        self.role = PromptSection(prefix="Role:", content=role)
        self.add_section(name="role", section=self.role)
        self._sections.move_to_end("role", last=False)


class ZeroShotEmotionPrompt(ZeroShotPrompt):
    def __init__(self, instructions: PromptSection, emotion: str) -> None:
        super().__init__(instructions)
        self.emotion = PromptSection(prefix="Emotion:", content=emotion)
        self.add_section(name="emotion", section=self.emotion)
