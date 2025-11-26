Requesting pytest-fixtures
==========================
.. External references
.. _pytest-fixtures: https://docs.pytest.org/en/6.2.x/fixture.html

`pytest-fixtures`_ examples.

`pytest-fixtures`_ example for `.. code-block::` directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: rst

    .. pytestfixture: tmp_path
    .. pytestfixture: http_request
    .. code-block:: python
        :name: test_path_and_http_request

        d = tmp_path / "sub"
        d.mkdir()  # Create the directory
        assert d.is_dir()  # Verify it was created and is a directory

        assert isinstance(http_request.GET, dict)
