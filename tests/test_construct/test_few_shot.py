import pytest
from construct.base import PromptSection, Example
from construct.few_shot import FewShotPrompt

def test_few_shot_prompt():
    instructions = PromptSection(content="Classify the sentiment.")
    example1 = Example(name="Positive", content="Input: I love it! Output: Positive")
    
    prompt = FewShotPrompt(instructions=instructions)
    prompt.add_example(example1)
    
    compiled = prompt.compile()
    # When compiling FewShotPrompt, it adds an 'examples' section.
    assert "examples" in prompt.all_sections()
    assert "Examples:\nInput: I love it! Output: Positive" in compiled
    assert "Classify the sentiment." in compiled

def test_few_shot_prompt_with_initial_examples():
    instructions = PromptSection(content="Classify.")
    examples = [Example(name="e1", content="c1"), Example(name="e2", content="c2")]
    
    prompt = FewShotPrompt(instructions=instructions, examples=examples)
    compiled = prompt.compile()
    
    assert "Examples:\nc1\n\nc2" in compiled
