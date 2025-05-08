In the example below:

- `moto`_ is used to mock AWS S3 service for all tests marked as ``aws``.
- Environment variable ``OPENAI_BASE_URL`` is set
  to ``http://localhost:11434/v1`` (assuming you have `Ollama`_ running) for
  all tests marked as ``openai``.
- ``FILE_REGISTRY.clean_up()`` is executed at the end of each test marked
  as ``fakepy``.

*Filename: conftest.py*

.. code-block:: python

    import os
    from contextlib import suppress

    import pytest

    from fake import FILE_REGISTRY
    from moto import mock_aws
    from pytest_codeblock.constants import CODEBLOCK_MARK

    # Modify test item during collection
    def pytest_collection_modifyitems(config, items):
        for item in items:
            if item.get_closest_marker(CODEBLOCK_MARK):
                # All `pytest-codeblock` tests are automatically assigned
                # a `codeblock` marker, which can be used for customisation.
                # In the example below we add an additional `documentation`
                # marker to `pytest-codeblock` tests.
                item.add_marker(pytest.mark.documentation)
            if item.get_closest_marker("aws"):
                # Apply `mock_aws` to all tests marked as `aws`
                item.obj = mock_aws(item.obj)


    # Setup before test runs
    def pytest_runtest_setup(item):
        if item.get_closest_marker("openai"):
            # Send all OpenAI requests to locally running Ollama for all
            # tests marked as `openai`. The tests would x-pass on environments
            # where Ollama is up and running (assuming, you have created an
            # alias for gpt-4o using one of the available models) and would
            # x-fail on environments, where Ollama isn't runnig.
            os.environ.setdefault("OPENAI_API_KEY", "ollama")
            os.environ.setdefault("OPENAI_BASE_URL", "http://localhost:11434/v1")


    # Teardown after the test ends
    def pytest_runtest_teardown(item, nextitem):
        # Run file clean up on all tests marked as `fakepy`
        if item.get_closest_marker("fakepy"):
            FILE_REGISTRY.clean_up()