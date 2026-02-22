# Technologies Used in Crocoprompt Testing

This document explains the tools and frameworks used for testing the Crocoprompt module, providing Minimal Reproducible Examples (MREs) for future reference.

## 1. Pytest

**Pytest** is a robust and scalable testing framework for Python. It simplifies writing test cases with its clean syntax centered around Python's native `assert` statement and rich ecosystem of fixtures.

**Why we use it:**
- Minimal boilerplate (no need for `unittest.TestCase` classes).
- Built-in support for test discovery (`test_*.py` files).
- Fixtures for powerful setup and teardown mechanisms.

### MRE: Pytest Basics

Create a file named `test_math.py`:

```python
import pytest

# A simple function to test
def add(a, b):
    return a + b

# Basic arithmetic test
def test_addition():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

# Using fixtures for shared resources
@pytest.fixture
def sample_data():
    return {"user": "admin", "id": 42}

def test_data(sample_data):
    assert sample_data["id"] == 42
```

Run the tests from your terminal:
```bash
pytest test_math.py
```

## 2. GitHub Actions

**GitHub Actions** is a CI/CD (Continuous Integration / Continuous Deployment) platform that allows you to automate your build, test, and deployment pipelines directly within GitHub.

**Why we use it:**
- Automates running `pytest` on every push or Pull Request.
- Ensures new features or refactors don't break existing tests.
- Integrates securely and simply with GitHub repositories.

### MRE: Simple GitHub Action

Create a file `.github/workflows/python-app.yml` in your repository:

```yaml
name: Python application testing

# Controls when the workflow will run
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

# A workflow run is made up of one or more jobs
jobs:
  build:
    runs-on: ubuntu-latest # Operating system

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
    # 1. Checkout the repository code
    - uses: actions/checkout@v4

    # 2. Setup Python environment
    - name: Set up Python 3.10
      uses: actions/setup-python@v5
      with:
        python-version: "3.10"

    # 3. Install dependencies
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest

    # 4. Run tests
    - name: Test with pytest
      run: |
        pytest
```

## Running crocoprompt tests locally
We manage our dependencies with `uv`. To run tests locally, you can use:

```bash
uv run pytest tests/
```
