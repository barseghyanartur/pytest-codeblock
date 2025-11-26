from types import SimpleNamespace

import pytest


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
