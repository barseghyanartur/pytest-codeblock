More pytest-fixtures, including nested ones
===========================================
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

Then again:

.. code-block:: rst

    .. pytestfixture: tmp_path
    .. pytestfixture: http_request
    .. code-block:: python
        :name: test_path_and_http_request_2

        d = tmp_path / "sub"
        d.mkdir()  # Create the directory
        assert d.is_dir()  # Verify it was created and is a directory

        assert isinstance(http_request.GET, dict)

`pytest-fixtures`_ example for `.. literalinclude::` directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: rst

    .. pytestfixture: tmp_path
    .. pytestfixture: http_request
    .. literalinclude:: examples/python/tmp_path_example.py
        :name: test_path_example

Then again:

.. code-block:: rst

    .. pytestfixture: tmp_path
    .. pytestfixture: http_request
    .. literalinclude:: examples/python/tmp_path_example.py
        :name: test_path_example_2

`pytest-fixtures`_ example for nested `.. literalinclude::` directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. pytestfixture: tmp_path
.. pytestfixture: http_request
.. literalinclude:: examples/python/tmp_path_example.py
    :name: test_path_example_3

Then again:

.. code-block:: rst

    .. pytestfixture: tmp_path
    .. pytestfixture: http_request
    .. literalinclude:: examples/python/tmp_path_example.py
        :name: test_path_example_4
