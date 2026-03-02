from crocoprompt.construct.base import PromptSection
from crocoprompt.construct.thought.cok import ChainOfKnowledge, Triplet
from crocoprompt.construct.thought.cot.base import ChainOfThoughtPrompt
from crocoprompt.construct.thought.cot.cue_cot import CueChainOfThoughtPrompt


def test_chain_of_knowledge():
    instructions = PromptSection(content="Answer the question.")
    triplets = [Triplet(items=["Apple", "is", "fruit"]), Triplet(items=["Sky", "is", "blue"])]
    explanation = PromptSection(content="Based on the above knowledge, answer.")

    prompt = ChainOfKnowledge(instructions=instructions, knowledge_triplets=triplets, explanation=explanation)

    sections = prompt.all_sections()
    assert "instructions" in sections
    assert "knowledge_triplets" in sections
    assert "explanation" in sections

    compiled = prompt.compile()
    assert "['Apple', 'is', 'fruit']\n\n['Sky', 'is', 'blue']" in compiled


def test_chain_of_thought_prompt():
    instructions = PromptSection(content="Solve the math problem.")
    thinking = PromptSection(content="Let's think step by step.")

    prompt = ChainOfThoughtPrompt(instructions=instructions, thinking=thinking)

    sections = prompt.all_sections()
    assert "instructions" in sections
    assert "thinking" in sections
    assert prompt.compile() == "Solve the math problem.\n\nLet's think step by step."


def test_cue_chain_of_thought_prompt():
    instructions = PromptSection(content="Solve this.")
    thinking = PromptSection(content="Thinking Process:")
    cue = PromptSection(content="First,")

    prompt = CueChainOfThoughtPrompt(instructions=instructions, thinking=thinking, cue=cue)

    sections = prompt.all_sections()
    assert "cue" in sections
    compiled = prompt.compile()
    assert "First," in compiled
