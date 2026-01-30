================
pytest-codeblock
================

.. External references
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _Markdown: https://daringfireball.net/projects/markdown/
.. _pytest: https://docs.pytest.org
.. _Django: https://www.djangoproject.com
.. _pip: https://pypi.org/project/pip/
.. _uv: https://pypi.org/project/uv/
.. _fake.py: https://github.com/barseghyanartur/fake.py
.. _boto3: https://github.com/boto/boto3
.. _moto: https://github.com/getmoto/moto
.. _openai: https://github.com/openai/openai-python
.. _Ollama: https://github.com/ollama/ollama
.. _tomli: https://pypi.org/project/tomli/

.. Internal references

.. _pytest-codeblock: https://github.com/barseghyanartur/pytest-codeblock/
.. _Read the Docs: http://pytest-codeblock.readthedocs.io/
.. _Examples: https://github.com/barseghyanartur/pytest-codeblock/tree/main/examples
.. _Customisation docs: https://pytest-codeblock.readthedocs.io/en/latest/customisation.html
.. _Contributor guidelines: https://pytest-codeblock.readthedocs.io/en/latest/contributor_guidelines.html
.. _reStructuredText docs: https://pytest-codeblock.readthedocs.io/en/latest/restructured_text.html
.. _Markdown docs: https://pytest-codeblock.readthedocs.io/en/latest/markdown.html
.. _llms.txt: https://barseghyanartur.github.io/pytest-codeblock/llms.txt

Test your documentation code blocks.

.. image:: https://img.shields.io/pypi/v/pytest-codeblock.svg
   :target: https://pypi.python.org/pypi/pytest-codeblock
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/pytest-codeblock.svg
    :target: https://pypi.python.org/pypi/pytest-codeblock/
    :alt: Supported Python versions

.. image:: https://github.com/barseghyanartur/pytest-codeblock/actions/workflows/test.yml/badge.svg?branch=main
   :target: https://github.com/barseghyanartur/pytest-codeblock/actions
   :alt: Build Status

.. image:: https://readthedocs.org/projects/pytest-codeblock/badge/?version=latest
    :target: http://pytest-codeblock.readthedocs.io
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/docs-llms.txt-blue
    :target: http://pytest-codeblock.readthedocs.io/en/latest/llms.txt
    :alt: llms.txt - documentation for LLMs

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/barseghyanartur/pytest-codeblock/#License
   :alt: MIT

.. image:: https://coveralls.io/repos/github/barseghyanartur/pytest-codeblock/badge.svg?branch=main&service=github
    :target: https://coveralls.io/github/barseghyanartur/pytest-codeblock?branch=main
    :alt: Coverage

`pytest-codeblock`_ is a `Pytest`_ plugin that discovers Python code examples
in your `reStructuredText`_ and `Markdown`_ documentation files and runs them
as part of your test suite. This ensures your docs stay correct and up-to-date.

Features
========

- **reStructuredText and Markdown support**: Automatically find and test code
  blocks in `reStructuredText`_ (``.rst``) and `Markdown`_ (``.md``) files.
  The only requirement here is that your code blocks shall
  have a name starting with ``test_``. Async code snippets are supported as
  well.
- **Grouping**: Split a single example across multiple code blocks;
  the plugin concatenates them into one test.
- **Pytest markers support**: Add existing or custom `pytest`_ markers
  to the code blocks and hook into the tests life-cycle using ``conftest.py``.
- **Pytest fixtures support**: Request existing or custom `pytest`_ fixtures
  for the code blocks.

Prerequisites
=============
- Python 3.10+
- `pytest`_ is the only required dependency (on Python 3.11+; for Python 3.10
  `tomli`_ is also required).

Documentation
=============
- Documentation is available on `Read the Docs`_.
- For `reStructuredText`_, see a dedicated `reStructuredText docs`_.
- For `Markdown`_, see a dedicated `Markdown docs`_.
- Both `reStructuredText docs`_ and `Markdown docs`_ have extensive
  documentation on `pytest`_ markers and corresponding ``conftest.py`` hooks.
- For guidelines on contributing check the `Contributor guidelines`_.

Installation
============

Install with `pip`_:

.. code-block:: sh

    pip install pytest-codeblock

Or install with `uv`_:

.. code-block:: sh

    uv pip install pytest-codeblock

.. _configuration:

Configuration
=============
For most use cases, no configuration needed. All your `.rst` and `.md` files
shall be picked automatically.

However, if you need to add another file extension or use or another language
identifier for python in codeblock, you could configure that.

See the following example of `pyproject.toml` configuration:

*Filename: pyproject.toml*

.. code-block:: toml

    [tool.pytest-codeblock]
    rst_user_codeblocks = ["c_py"]
    rst_user_extensions = [".rst.txt"]
    md_user_codeblocks = ["c_py"]
    md_user_extensions = [".md.txt"]

See `customisation docs`_ for more.

Usage
=====
reStructruredText usage
-----------------------
Any code directive, such as ``.. code-block:: python``, ``.. code:: python``,
or literal blocks with a preceding ``.. codeblock-name: <name>``, will be
collected and executed automatically by `pytest`_.

``code-block`` directive example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: Note that ``:name:`` value has a ``test_`` prefix.

*Filename: README.rst*

.. code-block:: rst

    .. code-block:: python
       :name: test_basic_example

       import math

       result = math.pow(3, 2)
       assert result == 9


``literalinclude`` directive example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: Note that ``:name:`` value has a ``test_`` prefix.

*Filename: README.rst*

.. code-block:: rst

    .. literalinclude:: examples/python/basic_example.py
        :name: test_li_basic_example

See a dedicated `reStructuredText docs`_ for more.

Markdown usage
--------------

Any fenced code block with a recognized Python language tag (e.g., ``python``,
``py``) will be collected and executed automatically by `pytest`_.

.. note:: Note that ``name`` value has a ``test_`` prefix.

*Filename: README.md*

.. code-block:: markdown

    ```python name=test_basic_example
    import math

    result = math.pow(3, 2)
    assert result == 9
    ```

See a dedicated `Markdown docs`_ for more.

Tests
=====

Run the tests with `pytest`_:

.. code-block:: sh

    pytest

Troubleshooting
===============
If something doesn't work, try to add this to your pyproject.toml:

*Filename: pyproject.toml*

.. code-block:: text

    [tool.pytest.ini_options]
    testpaths = [
        "**/*.rst",
        "**/*.md",
    ]

Writing documentation
=====================

Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======

MIT

Support
=======
For security issues contact me at the e-mail given in the `Author`_ section.

For overall issues, go
to `GitHub <https://github.com/barseghyanartur/pytest-codeblock/issues>`_.

Author
======

Artur Barseghyan <artur.barseghyan@gmail.com>
