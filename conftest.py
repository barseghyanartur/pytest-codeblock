import pytest
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
