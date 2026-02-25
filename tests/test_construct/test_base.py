from construct.base import Example, PromptSection, SectionPrompt


def test_prompt_section_render():
    section = PromptSection(content="Hello {name}", variables={"name": "World"})
    assert section.render() == "Hello World"


def test_prompt_section_render_with_prefix_suffix():
    section = PromptSection(content="Middle", prefix="Start:", suffix=":End")
    assert section.render() == "Start:\nMiddle\n:End"


def test_prompt_section_format():
    section = PromptSection(content="Hello {} and {name}")
    assert section.format("Alice", name="Bob") == "Hello Alice and Bob"


def test_prompt_section_str():
    section = PromptSection(content="Content", prefix="Prefix", suffix="Suffix")
    assert str(section) == "Prefix\nContent\nSuffix"


def test_example_dataclass():
    example = Example(name="Ex1", content="Some content")
    assert example.name == "Ex1"
    assert example.content == "Some content"


def test_section_prompt():
    prompt = SectionPrompt(section1=PromptSection(content="Content 1"), section2=PromptSection(content="Content 2"))

    assert prompt.compile() == "Content 1\n\nContent 2"
    assert prompt.compile(order=["section2", "section1"]) == "Content 2\n\nContent 1"

    prompt.add_section("section3", PromptSection(content="Content 3"))
    assert "section3" in prompt.all_sections()
    assert prompt.get_section("section3").content == "Content 3"
