import contextlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest
import respx
from fake import FILE_REGISTRY
from moto import mock_aws

from pytest_codeblock.constants import CODEBLOCK_MARK

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "http_request",
    "http_request_factory",
    "markdown_simple",
    "markdown_with_pytest_mark",
    "openai_mock",
    "pytest_collection_modifyitems",
    "pytest_runtest_setup",
    "pytest_runtest_teardown",
)

pytest_plugins = ["pytester"]


# Modify test item during collection
def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Modify collected test items after collection is done.

    :param config: The pytest configuration object.
    :param items: A list of collected test items.
    """
    for item in items:
        if item.get_closest_marker(CODEBLOCK_MARK):
            # Add `documentation` marker to `pytest-codeblock` tests
            item.add_marker(pytest.mark.documentation)
        if item.get_closest_marker("aws"):
            # Apply `mock_aws` to all tests marked as `aws`
            item.obj = mock_aws(item.obj)


# Setup before test runs
def pytest_runtest_setup(item: pytest.Item) -> None:
    """Set up test environment before each test runs.

    :param item: The test item that is about to run.
    """


# Teardown after the test ends
def pytest_runtest_teardown(item: pytest.Item, nextitem: pytest.Item) -> None:
    """Tear down test environment after each test ends.

    :param item: The test item that just finished running.
    :param nextitem: The next test item that will run (or None if this is
    """
    if item.get_closest_marker("fakepy"):
        FILE_REGISTRY.clean_up()


@pytest.fixture
def http_request_factory():
    """
    Returns a function that creates a simple namespace object
    with a 'GET' attribute set to the provided dictionary.
    """
    def _factory(get_data: dict):
        # Creates an object like: object(GET={'key': 'value'})
        return SimpleNamespace(GET=get_data)
    return _factory


@pytest.fixture
def http_request(http_request_factory):
    test_data = {"param1": "value1", "signature": "mock-sig"}
    return http_request_factory(test_data)


@pytest.fixture
def openai_mock():
    # Setup
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
    yield mock

    # Teardown
    with contextlib.suppress(Exception):
        mock.stop()


@pytest.fixture
def markdown_simple():
    return """
```python name=test_example
x=1
assert x==1
```"""


@pytest.fixture
def markdown_with_pytest_mark():
    return """
<!-- pytestmark: django_db -->
```python name=test_db
from django.db import models
```"""


@pytest.fixture
def pytester_subprocess(pytester):
    """
    Wrapper that forces subprocess mode to avoid deprecation warning conflicts
    when the plugin uses the old `path` argument signature.
    """
    pytester.runpytest = pytester.runpytest_subprocess
    return pytester
