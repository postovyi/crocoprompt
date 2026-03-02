# crocoprompt

A prompt engineering toolkit for structured LLM prompt construction and format conversion.

[![PyPI version](https://badge.fury.io/py/crocoprompt.svg)](https://badge.fury.io/py/crocoprompt)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Installation

```bash
pip install crocoprompt
```

## Quick Start

```python
from crocoprompt import ZeroShotPrompt, MarkdownConverter
from crocoprompt.construct.base import PromptSection

prompt = ZeroShotPrompt(
    instructions=PromptSection(content="Summarise the following article in three bullet points.")
)
print(MarkdownConverter.convert(prompt))
# # Instructions
# Summarise the following article in three bullet points.
```

## Core Concepts

### PromptSection

The fundamental building block of all prompts. Represents a single section with optional variable substitution and wrapping:

```python
from crocoprompt.construct.base import PromptSection

section = PromptSection(
    content="Hello {name}",
    variables={"name": "World"},
    prefix="Greeting:",
)
print(section.render())  # Greeting:\nHello World
```

### SectionPrompt

A prompt composed of named `PromptSection` objects, compiled by joining sections with double newlines:

```python
from crocoprompt.construct.base import PromptSection, SectionPrompt

prompt = SectionPrompt(
    role=PromptSection(content="You are a helpful assistant."),
    task=PromptSection(content="Translate to Spanish."),
)
print(prompt.compile())
```

## Prompt Strategies

### Zero-Shot

Plain instructions without examples.

| Class | Description |
|---|---|
| `ZeroShotPrompt` | Plain instructions only |
| `ZeroShotRolePrompt` | Instructions + role prefix |
| `ZeroShotEmotionPrompt` | Instructions + emotion suffix |

```python
from crocoprompt import ZeroShotRolePrompt
from crocoprompt.construct.base import PromptSection

prompt = ZeroShotRolePrompt(
    instructions=PromptSection(content="Translate to French."),
    role="Expert Translator",
)
print(prompt.compile())
# Role: Expert Translator
# 
# Translate to French.
```

### Few-Shot

Instructions with labelled examples to demonstrate the expected pattern:

```python
from crocoprompt import FewShotPrompt
from crocoprompt.construct.base import PromptSection, Example

prompt = FewShotPrompt(
    instructions=PromptSection(content="Classify the sentiment."),
    examples=[
        Example(name="pos", content="Input: I love it! Output: Positive"),
        Example(name="neg", content="Input: Terrible. Output: Negative"),
    ],
)
print(prompt.compile())
```

### Chain-of-Thought

Explicit step-by-step reasoning section to encourage better outputs:

```python
from crocoprompt import ChainOfThoughtPrompt
from crocoprompt.construct.base import PromptSection

prompt = ChainOfThoughtPrompt(
    instructions=PromptSection(content="What is 7 * 8?"),
    thinking=PromptSection(content="Let's think step by step."),
)
print(prompt.compile())
```

### Cue-based Chain-of-Thought

Chain-of-Thought augmented with a partial answer scaffold:

```python
from crocoprompt import CueChainOfThoughtPrompt
from crocoprompt.construct.base import PromptSection

prompt = CueChainOfThoughtPrompt(
    instructions=PromptSection(content="Solve this."),
    thinking=PromptSection(content="Let's think step by step."),
    cue=PromptSection(content="First, I notice that"),
)
print(prompt.compile())
```

### Chain-of-Knowledge

Instructions grounded by structured knowledge triplets:

```python
from crocoprompt import ChainOfKnowledge, Triplet
from crocoprompt.construct.base import PromptSection

prompt = ChainOfKnowledge(
    instructions=PromptSection(content="Answer the question."),
    knowledge_triplets=[
        Triplet(items=["Paris", "is capital of", "France"]),
        Triplet(items=["France", "is in", "Europe"]),
    ],
    explanation=PromptSection(content="Use the above facts."),
)
print(prompt.compile())
```

## Output Converters

Convert compiled prompts to different formats for various platforms.

| Converter | Output Format |
|---|---|
| `MarkdownConverter` | Markdown with headers (`# Section`) |
| `XMLConverter` | XML tags (`<section>`) |
| `YAMLConverter` | YAML block scalars (`section: |`) |

```python
from crocoprompt import (
    SectionPrompt,
    MarkdownConverter,
    XMLConverter,
    YAMLConverter,
)
from crocoprompt.construct.base import PromptSection

prompt = SectionPrompt(
    role=PromptSection(content="You are a helpful assistant."),
    task=PromptSection(content="Translate the text to Spanish."),
)

# Markdown output
print(MarkdownConverter.convert(prompt))
# # Role
# You are a helpful assistant.
#
# # Task
# Translate the text to Spanish.

# XML output
print(XMLConverter.convert(prompt))
# <role>
# You are a helpful assistant.
# </role>
#
# <task>
# Translate the text to Spanish.
# </task>

# YAML output
print(YAMLConverter.convert(prompt))
# role: |
#   You are a helpful assistant.
#
# task: |
#   Translate the text to Spanish.
```

### Custom Section Order

Control the order of sections in the output:

```python
prompt = SectionPrompt(
    a=PromptSection(content="A"),
    b=PromptSection(content="B"),
)

# Default insertion order
print(prompt.compile())  # A\n\nB

# Custom order
print(prompt.compile(order=["b", "a"]))  # B\n\nA

# Works with converters too
print(XMLConverter.convert(prompt, order=["b", "a"]))
```

## Examples

### Sentiment Analysis Prompt

```python
from crocoprompt import FewShotPrompt, MarkdownConverter
from crocoprompt.construct.base import PromptSection, Example

sentiment_prompt = FewShotPrompt(
    instructions=PromptSection(
        content="Classify the sentiment of the following text.",
    ),
    examples=[
        Example(
            name="positive",
            content="Input: I absolutely love this product!\nOutput: Positive",
        ),
        Example(
            name="negative",
            content="Input: This is the worst experience ever.\nOutput: Negative",
        ),
        Example(
            name="neutral",
            content="Input: The weather is cloudy today.\nOutput: Neutral",
        ),
    ],
)

print(MarkdownConverter.convert(sentiment_prompt))
```

### Complex Reasoning Task

```python
from crocoprompt import (
    ChainOfKnowledge,
    CueChainOfThoughtPrompt,
    XMLConverter,
)
from crocoprompt.construct.base import PromptSection, Triplet

reasoning_prompt = ChainOfKnowledge(
    instructions=PromptSection(
        content="Based on the facts provided, answer: Is Paris the capital of France?",
    ),
    knowledge_triplets=[
        Triplet(items=["Paris", "is capital of", "France"]),
        Triplet(items=["France", "is in", "Europe"]),
    ],
    explanation=PromptSection(
        content="Use the knowledge above to construct your answer.",
    ),
)

print(XMLConverter.convert(reasoning_prompt))
```

## API Reference

### Data Structures

- `PromptSection`: A single prompt section with content, variables, prefix, and suffix
- `Example`: A named example used in few-shot learning
- `SectionPrompt`: A prompt composed of named sections
- `Triplet`: A knowledge triplet (subject, predicate, object)

### Prompt Classes

- `ZeroShotPrompt`: Plain zero-shot
- `ZeroShotRolePrompt`: Zero-shot with role context
- `ZeroShotEmotionPrompt`: Zero-shot with emotional framing
- `FewShotPrompt`: Few-shot with examples
- `ChainOfThoughtPrompt`: Chain-of-Thought reasoning
- `CueChainOfThoughtPrompt`: CoT with answer cue
- `ChainOfKnowledge`: Knowledge-grounded reasoning

### Converters

- `MarkdownConverter`: Convert to Markdown format
- `XMLConverter`: Convert to XML format
- `YAMLConverter`: Convert to YAML format

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues on [GitHub](https://github.com/postovyi/crocoprompt).

## License

MIT License — see [LICENSE](LICENSE) for details.
