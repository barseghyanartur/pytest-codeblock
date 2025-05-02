import os

import pytest
from fake import FILE_REGISTRY
from moto import mock_aws

from pytest_codeblock.constants import CODEBLOCK_MARK


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
        # Send all OpenAI requests to locally running Ollama
        os.environ.setdefault("OPENAI_API_KEY", "ollama")
        # os.environ.setdefault("OPENAI_BASE_URL", "http://localhost:11434/v1")


# Teardown after the test ends
def pytest_runtest_teardown(item, nextitem):
    # Run file clean up on all tests marked as `fakepy`
    if item.get_closest_marker("fakepy"):
        FILE_REGISTRY.clean_up()
