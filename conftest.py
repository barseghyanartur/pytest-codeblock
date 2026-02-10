import json
import os
from pathlib import Path

import pytest
import respx
from fake import FILE_REGISTRY
from moto import mock_aws

from pytest_codeblock.constants import CODEBLOCK_MARK

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "pytest_collection_modifyitems",
    "pytest_runtest_setup",
    "pytest_runtest_teardown",
)


# Modify test item during collection
def pytest_collection_modifyitems(config, items):
    for item in items:
        if item.get_closest_marker(CODEBLOCK_MARK):
            # Add `documentation` marker to `pytest-codeblock` tests
            item.add_marker(pytest.mark.documentation)
        if item.get_closest_marker("aws"):
            # Apply `mock_aws` to all tests marked as `aws`
            item.obj = mock_aws(item.obj)


# Setup before test runs
def pytest_runtest_setup(item):
    if item.get_closest_marker("openai"):
        os.environ.setdefault("OPENAI_API_KEY", "test-key")
        cassette_path = (
            Path(__file__).parent
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
        item._openai_mock = mock


# Teardown after the test ends
def pytest_runtest_teardown(item, nextitem):
    # Stop respx mock for openai tests
    if hasattr(item, "_openai_mock"):
        item._openai_mock.stop()
        del item._openai_mock
    # Run file clean up on all tests marked as `fakepy`
    if item.get_closest_marker("fakepy"):
        FILE_REGISTRY.clean_up()
