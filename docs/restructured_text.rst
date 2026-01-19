reStructuredText
================

.. External references
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _pytest: https://docs.pytest.org
.. _Django: https://www.djangoproject.com
.. _pip: https://pypi.org/project/pip/
.. _uv: https://pypi.org/project/uv/
.. _fake.py: https://github.com/barseghyanartur/fake.py
.. _boto3: https://github.com/boto/boto3
.. _moto: https://github.com/getmoto/moto
.. _openai: https://github.com/openai/openai-python
.. _Ollama: https://github.com/ollama/ollama

The following directives are supported:

- ``.. code-block:: python``
- ``.. code:: python``
- ``.. codeblock-name: <name>``
- ``.. literalinclude::``

Any code directive, such as ``.. code-block:: python``, ``.. code:: python``,
``.. literalinclude::`` or literal blocks with a
preceding ``.. codeblock-name: <name>``, will be collected and executed
automatically, if your `pytest`_ :ref:`configuration <configuration>` allows
that.

Usage examples
--------------

Standalone code blocks
~~~~~~~~~~~~~~~~~~~~~~

``code-block`` directive
^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: Note that ``:name:`` value has a ``test_`` prefix.

*Filename: README.rst*

.. code-block:: rst

    .. code-block:: python
       :name: test_basic_example

       import math

       result = math.pow(3, 2)
       assert result == 9

----

``literalinclude`` directive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Filename: README.rst*

.. code-block:: rst

    .. literalinclude:: examples/python/basic_example.py
        :name: test_li_basic_example

----

``codeblock-name`` directive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also use a literal block with a preceding name comment:

*Filename: README.rst*

.. code-block:: rst

    .. codeblock-name: test_grouping_example_literal_block
    This is a literal block::

       y = 5
       print(y * 2)

----

Grouping multiple ``code-block`` directives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's possible to split one logical test into multiple blocks.
They will be tested under the first ``:name:`` specified.
Note the ``.. continue::`` directive.

.. note:: Note that ``continue`` directive of
          the ``test_grouping_example_part_2``
          and ``test_grouping_example_part_3`` refers to
          the ``test_grouping_example``.

*Filename: README.rst*

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

Adding pytest markers to ``code-block`` and ``literalinclude`` directives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's possible to add custom pytest markers to your ``code-block``
or ``literalinclude`` directives. That allows adding custom logic and mocking
in your ``conftest.py``.

In the example below, ``django_db`` marker is added to the ``code-block``
directive.

.. note:: Note the ``pytestmark`` directive ``django_db`` marker.

*Filename: README.rst*

.. code-block:: rst

    .. pytestmark: django_db
    .. code-block:: python
        :name: test_django

        from django.contrib.auth.models import User

        user = User.objects.first()

----

In the example below, ``django_db`` marker is added to the ``literalinclude``
directive.

*Filename: README.rst*

.. code-block:: rst

    .. pytestmark: django_db
    .. literalinclude:: examples/python/django_example.py
        :name: test_li_django_example

----

Requesting pytest fixtures for ``code-block`` and ``literalinclude`` directives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's possible to request existing or custom pytest fixtures in ``code-block``
or ``literalinclude`` directives. That allows adding custom logic and mocking
in ``conftest.py``.

In the example below, ``tmp_path`` fixture is requested for the ``code-block``
directive.

.. note:: Note the ``pytestfixture`` directive ``tmp_path`` fixture.

*Filename: README.rst*

.. code-block:: rst

    .. pytestfixture: tmp_path
    .. code-block:: python
        :name: test_path

        d = tmp_path / "sub"
        d.mkdir()  # Create the directory
        assert d.is_dir()  # Verify it was created and is a directory

----

In the example below, ``tmp_path`` fixture is requested for the ``literalinclude``
directive.

*Filename: README.rst*

.. code-block:: rst

    .. pytestfixture: tmp_path
    .. literalinclude:: examples/python/tmp_path_example.py
        :name: test_li_tmp_path_example

----

Multiple ``pytestfixture`` directives are supported. Add one on each line.

.. note::

    When combining ``pytestfixture`` and ``continue`` directives together,
    request pytest-fixtures only in the first ``code-block``, as they will
    automatically become available in all continuing blocks.

Custom pytest-fixtures are supported as well. Just define them in
your ``conftest.py`` file.

Customisation/hooks
-------------------
Tests can be extended and fine-tuned using `pytest`_'s standard hook system.

Below is an example workflow:

1. **Add custom pytest markers** to the ``code-block``
   or ``literalinclude`` (``fakepy``, ``aws``, ``openai``).
2. **Implement pytest hooks** in ``conftest.py`` to react to those markers.

Add custom pytest markers
~~~~~~~~~~~~~~~~~~~~~~~~~

Add ``fakepy`` marker
^^^^^^^^^^^^^^^^^^^^^

The example code below will generate a PDF file with random text
using `fake.py`_ library. Note, that a ``fakepy`` marker is added to
the ``code-block``.

In the `Implement pytest hooks`_ section, you will see what can be done
with the markers.

.. note:: Note the ``pytestmark`` directive ``fakepy`` marker.

*Filename: README.rst*

.. code-block:: rst

    .. pytestmark: fakepy
    .. code-block:: python
        :name: test_create_pdf_file

        from fake import FAKER

        FAKER.pdf_file()

----

In the example code below, a ``fakepy`` marker is added to
the ``literalinclude`` block.

*Filename: README.rst*

.. code-block:: rst

    .. pytestmark: fakepy
    .. literalinclude:: examples/python/create_pdf_file_example.py
        :name: test_li_create_pdf_file

----

Add ``aws`` marker
^^^^^^^^^^^^^^^^^^

Sample `boto3`_ code to create a bucket on AWS S3.

.. note:: Note the ``pytestmark`` directive ``aws`` marker.

*Filename: README.rst*

.. code-block:: rst

    .. pytestmark: aws
    .. code-block:: python
        :name: test_create_bucket

        import boto3

        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="my-bucket")
        assert "my-bucket" in [b["Name"] for b in s3.list_buckets()["Buckets"]]

----

Add ``openai`` marker
^^^^^^^^^^^^^^^^^^^^^

Sample `openai`_ code to ask LLM to tell a joke. Note, that next to a
custom ``openai`` marker, ``xfail`` marker is used, which allows underlying
code to fail, without marking entire test suite as failed.

.. note:: Note the ``pytestmark`` directive ``xfail`` and ``openai`` markers.

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

----

Implement pytest hooks
~~~~~~~~~~~~~~~~~~~~~~

.. include:: _implement_pytest_hooks.rst

----

Async
~~~~~

You can use `top-level await` in your code blocks. The code will be
automatically wrapped in an async function.

*Filename: README.rst*

.. code-block:: rst

    .. code-block:: python
        :name: test_async_example

        import asyncio

        result = await asyncio.sleep(0.1, result=42)
        assert result == 42
