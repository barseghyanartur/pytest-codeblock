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
- **Support for literalinclude blocks** in `.rst` files.
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
        "**/*.rst",
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

----

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

----

**pytest marks**

In the example below, `django_db` marker is added to the code.

.. code-block:: rst

    .. pytestmark: django_db
    .. code-block:: python
        :name: test_django

        from django.contrib.auth.models import User

        user = User.objects.first()

----

**literalinclude**

.. code-block:: rst

    .. pytestmark: fakepy
    .. literalinclude:: examples/python/create_pdf_file_example.py
        :name: test_li_create_pdf_file

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

Customisation/hooks
===================
Tests can be extended and fine-tuned using `pytest`_'s standard hook system.

Below is an example workflow:

1. **Add custom markers** to the code blocks (``fakepy``, ``aws``, ``openai``).
2. **Implement pytest hooks** in ``conftest.py`` to react to those markers.


Add custom markers in reStructuredText
--------------------------------------

``fakepy`` reStructuredText marker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample `fake.py`_ code to generate a PDF file with random text.

*Filename: README.rst*

.. code-block:: rst

    .. pytestmark: fakepy
    .. code-block:: python
        :name: test_create_pdf_file

        from fake import FAKER

        FAKER.pdf_file()

``aws`` reStructuredText marker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample `boto3`_ code to create a bucket on AWS S3.

*Filename: README.rst*

.. code-block:: rst

    .. pytestmark: aws
    .. code-block:: python
        :name: test_create_bucket

        import boto3

        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="my-bucket")
        assert "my-bucket" in [b["Name"] for b in s3.list_buckets()["Buckets"]]

``openai`` reStructuredText marker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample `openai`_ code to ask LLM to tell a joke. Note, that next to a
custom ``openai`` marker, ``xfail`` marker is used, which allows underlying
code to fail, without marking entire test suite as failed.

*Filename: README.rst*

.. code-block:: rst

    .. pytestmark: xfail
    .. pytestmark: openai
    .. code-block:: python
        :name: test_tell_me_a_joke

        from openai import OpenAI

        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a famous comedian."},
                {"role": "user", "content": "Tell me a joke."},
            ],
        )

        assert isinstance(completion.choices[0].message.content, str)

Add custom markers in Markdown
------------------------------

``fakepy`` Markdown marker
~~~~~~~~~~~~~~~~~~~~~~~~~~

*Filename: README.md*

.. code-block:: markdown

    <!-- pytestmark: fakepy -->
    ```python name=test_create_pdf_file
    from fake import FAKER

    FAKER.pdf_file()
    ```

``aws`` Markdown marker
~~~~~~~~~~~~~~~~~~~~~~~

*Filename: README.md*

.. code-block:: markdown

    <!-- pytestmark: aws -->
    ```python name=test_create_bucket
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="my-bucket")
    assert "my-bucket" in [b["Name"] for b in s3.list_buckets()["Buckets"]]
    ```

``openai`` Markdown marker
~~~~~~~~~~~~~~~~~~~~~~~~~~

*Filename: README.md*

.. code-block:: markdown

    <!-- pytestmark: xfail -->
    <!-- pytestmark: openai -->
    ```python name=test_tell_me_a_joke
    from openai import OpenAI

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": "You are a famous comedian."},
            {"role": "user", "content": "Tell me a joke."},
        ],
    )

    assert isinstance(completion.choices[0].message.content, str)
    ```

Implement pytest hooks
----------------------

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
