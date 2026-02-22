import pytest
from construct.base import PromptSection
from construct.zero_shot import ZeroShotPrompt, ZeroShotRolePrompt, ZeroShotEmotionPrompt

def test_zero_shot_prompt():
    instructions = PromptSection(content="Translate to French.")
    prompt = ZeroShotPrompt(instructions=instructions)
    
    assert "instructions" in prompt.all_sections()
    assert prompt.compile() == "Translate to French."

def test_zero_shot_role_prompt():
    instructions = PromptSection(content="Translate to French.")
    prompt = ZeroShotRolePrompt(instructions=instructions, role="Expert Translator")
    
    sections = prompt.all_sections()
    assert list(sections.keys()) == ["role", "instructions"]
    
    compiled = prompt.compile()
    assert "Role:\nExpert Translator" in compiled
    assert "Translate to French." in compiled
    assert compiled.startswith("Role:")

def test_zero_shot_emotion_prompt():
    instructions = PromptSection(content="Translate to French.")
    prompt = ZeroShotEmotionPrompt(instructions=instructions, emotion="You are very helpful.")
    
    sections = prompt.all_sections()
    assert list(sections.keys()) == ["instructions", "emotion"]
    
    compiled = prompt.compile()
    assert "Emotion:\nYou are very helpful." in compiled
    assert "Translate to French." in compiled
    assert compiled.endswith("helpful.")
