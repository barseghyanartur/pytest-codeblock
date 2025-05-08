Markdown
========

.. External references
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

Usage examples
--------------

Any fenced code block with a recognized Python language tag (e.g., ``python``,
``py``) will be collected and executed automatically, if
your `pytest`_ :ref:`configuration <configuration>` allows that.

Standalone code blocks
~~~~~~~~~~~~~~~~~~~~~~

.. note:: Note that ``name`` value has a ``test_`` prefix.

*Filename: README.md*

.. code-block:: markdown

    ```python name=test_basic_example
    import math

    result = math.pow(3, 2)
    assert result == 9
    ```

----

Grouping multiple code blocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's possible to split one logical test into multiple blocks by specifying
the same name.

.. note:: Note that both snippts share the same ``name``
          value (``test_grouping_example``).

*Filename: README.md*

.. code-block:: markdown

    ```python name=test_grouping_example
    x = 1
    ```

    Some intervening text.

    ```python name=test_grouping_example
    print(x + 1)  # Uses x from the first snippet
    ```

The above mentioned three snippets will run as a single test.

----

Adding pytest markers to code blocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's possible to add custom pytest markers to your code blocks. That allows
adding custom logic and mocking in your ``conftest.py``.

In the example below, ``django_db`` marker is added to the code block.

.. note:: Note the ``pytestmark`` directive ``django_db`` marker.

*Filename: README.md*

.. code-block:: markdown

    <!-- pytestmark: django_db -->
    ```python name=test_django
    from django.contrib.auth.models import User

    user = User.objects.first()
    ```

Customisation/hooks
-------------------
Tests can be extended and fine-tuned using `pytest`_'s standard hook system.

Below is an example workflow:

1. **Add custom pytest markers** to the code
   blocks (``fakepy``, ``aws``, ``openai``).
2. **Implement pytest hooks** in ``conftest.py`` to react to those markers.

Add custom pytest markers
~~~~~~~~~~~~~~~~~~~~~~~~~

Add ``fakepy`` marker
^^^^^^^^^^^^^^^^^^^^^

The example code below will generate a PDF file with random text
using `fake.py`_ library. Note, that a ``fakepy`` marker is added to
the code block.

In the `Implement pytest hooks`_ section, you will see what can be done
with the markers.

.. note:: Note the ``pytestmark`` directive ``fakepy`` marker.

*Filename: README.md*

.. code-block:: markdown

    <!-- pytestmark: fakepy -->
    ```python name=test_create_pdf_file
    from fake import FAKER

    FAKER.pdf_file()
    ```

Add ``aws`` marker
^^^^^^^^^^^^^^^^^^

Sample `boto3`_ code to create a bucket on AWS S3.

.. note:: Note the ``pytestmark`` directive ``aws`` marker.

*Filename: README.md*

.. code-block:: markdown

    <!-- pytestmark: aws -->
    ```python name=test_create_bucket
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="my-bucket")
    assert "my-bucket" in [b["Name"] for b in s3.list_buckets()["Buckets"]]
    ```

Add ``openai`` marker
^^^^^^^^^^^^^^^^^^^^^

Sample `openai`_ code to ask LLM to tell a joke. Note, that next to a
custom ``openai`` marker, ``xfail`` marker is used, which allows underlying
code to fail, without marking entire test suite as failed.

.. note:: Note the ``pytestmark`` directive ``xfail`` and ``openai`` markers.

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

----

Implement pytest hooks
~~~~~~~~~~~~~~~~~~~~~~

.. include:: _implement_pytest_hooks.rst
