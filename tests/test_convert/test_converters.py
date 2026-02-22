import pytest
from collections import OrderedDict
from construct.base import SectionPrompt, PromptSection
from convert.xml import XMLConverter
from convert.markdown import MarkdownConverter
from convert.yaml import YAMLConverter

@pytest.fixture
def sample_prompt():
    prompt = SectionPrompt(
        instructions=PromptSection(content="Write a poem about the sea."),
        examples=PromptSection(content="Example 1: The sea is blue."),
        role=PromptSection(content="You are a poet.")
    )
    return prompt

def test_xml_converter(sample_prompt):
    result = XMLConverter.convert(sample_prompt)
    assert "<instructions>\nWrite a poem about the sea.\n</instructions>" in result
    assert "<examples>\nExample 1: The sea is blue.\n</examples>" in result
    assert "<role>\nYou are a poet.\n</role>" in result

def test_xml_converter_custom_order(sample_prompt):
    result = XMLConverter.convert(sample_prompt, order=["role", "instructions"])
    assert result.startswith("<role>")
    assert "Write a poem" in result
    assert "<examples>" not in result

def test_markdown_converter(sample_prompt):
    result = MarkdownConverter.convert(sample_prompt)
    assert "# Instructions\nWrite a poem about the sea." in result
    assert "# Examples\nExample 1: The sea is blue." in result
    assert "# Role\nYou are a poet." in result

def test_markdown_converter_custom_order(sample_prompt):
    result = MarkdownConverter.convert(sample_prompt, order=["role", "examples"])
    assert result.startswith("# Role\n")
    assert "# Instructions" not in result

def test_yaml_converter(sample_prompt):
    result = YAMLConverter.convert(sample_prompt)
    assert "instructions: |\n  Write a poem about the sea." in result
    assert "examples: |\n  Example 1: The sea is blue." in result
    assert "role: |\n  You are a poet." in result

def test_yaml_converter_custom_order(sample_prompt):
    result = YAMLConverter.convert(sample_prompt, order=["instructions"])
    assert result == "instructions: |\n  Write a poem about the sea."
