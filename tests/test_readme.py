"""Execute the tutorial without changing tracked documentation."""

from pathlib import Path

import jupytext
import pytest
from nbconvert.preprocessors import ExecutePreprocessor


@pytest.mark.integration
def test_execute_readme(tmp_path):
    readme = Path(__file__).resolve().parents[1] / "README.md"
    notebook = jupytext.read(readme)
    ExecutePreprocessor(timeout=120, kernel_name="python3").preprocess(
        notebook, {"metadata": {"path": str(tmp_path)}}
    )
