import contextlib
import json
import os
from pathlib import Path

import pytest
import respx

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "openai_mock",
)


@pytest.fixture
def openai_mock():
    # Setup
    os.environ.setdefault("OPENAI_API_KEY", "test-key")
    cassette_path = (
        Path(__file__).parent.parent
        / "examples"
        / "cassettes"
        / "openai_chat_completion.json"
    )
    with open(cassette_path) as f:
        response_data = json.load(f)

    mock = respx.mock()
    mock.start()
    mock.post("https://api.openai.com/v1/chat/completions").respond(
        json=response_data,
    )
    yield mock

    # Teardown
    with contextlib.suppress(Exception):
        mock.stop()

