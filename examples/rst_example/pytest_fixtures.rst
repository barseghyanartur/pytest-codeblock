pytest-fixtures
===============
pytest-fixtures examples.

.. External references
.. _openai: https://github.com/openai/openai-python
.. _moto: https://docs.getmoto.org
.. _fake.py: https://github.com/barseghyanartur/fake.py

`fake.py`_ example for `.. code-block::` directive with pytest-fixtures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: rst

    .. pytestfixture: tmp_path
    .. pytestfixture: http_request
    .. code-block:: python
        :name: test_files

        d = tmp_path / "sub"
        d.mkdir()  # Create the directory
        assert d.is_dir()  # Verify it was created and is a directory

        assert isinstance(http_request.GET, dict)
