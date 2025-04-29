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

.. Internal references

.. _pytest-codeblock: https://github.com/barseghyanartur/pytest-codeblock/
.. _Read the Docs: http://pytest-codeblock.readthedocs.io/
.. _Examples: https://github.com/barseghyanartur/pytest-codeblock/tree/main/examples
.. _Contributor guidelines: https://pytest-codeblock.readthedocs.io/en/latest/contributor_guidelines.html

Test your code blocks.

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

- **Markdown and reST support**: Automatically finds fenced code blocks
  in `.md`/`.markdown` files and `.. code-block:: python` or literal blocks
  in `.rst` files.
- **Grouping by name**: Split a single example across multiple code blocks;
  the plugin concatenates them into one test.
- **Minimal dependencies**: Only requires `pytest`_.

Prerequisites
=============
Python 3.9+

Documentation
=============
- Documentation is available on `Read the Docs`_.

Installation
============

Install with `pip`_:

.. code-block:: sh

    pip install pytest-codeblock

Or install with `uv`_:

.. code-block:: sh

    uv pip install pytest-codeblock

Configuration
=============
*Filename: pyproject.toml*

.. code-block:: text

    [tool.pytest.ini_options]
    testpaths = [
        "*.rst",
        "**/*.rst",
        "*.md",
        "**/*.md",
    ]

Usage
=====
reStructruredText usage
-----------------------
Any code directive, such as ``.. code-block:: python``, ``.. code:: python``,
or literal blocks with a preceding ``.. codeblock-name: <name>``, will be
collected and executed automatically, if your `pytest`_ `configuration`_
allows that.

**Basic example**

.. code-block:: rst

    .. code-block:: python
       :name: test_basic_example

       import math

       result = math.pow(3, 2)
       assert result == 9

You can also use a literal block with a preceding name comment:

.. code-block:: rst

    .. codeblock-name: test_grouping_example_literal_block
    This is a literal block::

       y = 5
       print(y * 2)

**Grouping example**

It's possible to split one logical test into multiple blocks.
They will be tested under the first ``:name:`` specified.
Note the ``.. continue::`` directive.

.. code-block:: rst

    .. code-block:: python
       :name: test_grouping_example

       x = 1

    Some intervening text.

    .. continue: test_grouping_example
    .. code-block:: python
       :name: test_grouping_example_part_2

       y = x + 1  # Uses x from the first snippet
       assert y == 2

    Some intervening text.

    .. continue: test_grouping_example
    .. code-block:: python
       :name: test_grouping_example_part_3

       print(y)  # Uses y from the previous snippet

The above mentioned three snippets will run as a single test.

**pytest marks**

.. code-block:: rst

    .. pytestmark: django_db
    .. code-block:: python
        :name: test_django

        from django.contrib.auth.models import User

        user = User.objects.first()

Markdown usage
--------------

Any fenced code block with a recognized Python language tag (e.g., ``python``,
``py``) will be collected and executed automatically, if your `pytest`_
`configuration`_ allows that.

**Basic example**

.. code-block:: markdown

    ```python name=test_basic_example
    import math

    result = math.pow(3, 2)
    assert result == 9
    ```

**Grouping example**

.. code-block:: markdown

    ```python name=test_grouping_example
    x = 1
    ```

    Some intervening text.

    ```python name=test_grouping_example
    print(x + 1)  # Uses x from the first snippet
    ```

**pytest marks**

.. code-block:: markdown

    <!-- pytestmark: django_db -->
    ```python name=test_django
    from django.contrib.auth.models import User

    user = User.objects.first()
    ```

Tests
=====

Run the tests with `pytest`_:

.. code-block:: sh

    pytest

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
