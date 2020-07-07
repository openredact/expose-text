from pathlib import Path

import pytest


@pytest.fixture
def test_files():
    return Path(__file__).parent / "files"
