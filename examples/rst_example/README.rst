reStructuredText example project
================================

This is a minimal example showing how `pytest-codeblock` will discover
and run only Python snippets whose `:name:` starts with `test_`.

Simple assertion
----------------

.. code-block:: python
   :name: test_simple_assert

   # A trivial test that always passes
   assert 2 + 2 == 4

Multi-part example
------------------

It's possible to split one logical test into multiple blocks.
They will be tested under the first ``:name:`` specified.
Note the ``.. continue::`` directive.

.. code-block:: python
   :name: test_compute_square

   import math

Some intervening text.

.. continue: test_compute_square
.. code-block:: python
   :name: test_compute_square_part_2

   result = math.pow(3, 2)
   assert result == 9

Some intervening text.

.. continue: test_compute_square
.. code-block:: python
   :name: test_compute_square_part_3

   print(result)

Ignored snippets
----------------

Blocks without a `:name:` or without the `test_` prefix are **not** collected:

.. code-block:: python

   # No :name:, so this is ignored

.. code-block:: python
   :name: example_not_test

   # Name does not start with `test_`, so this is ignored

Non-Python blocks are also ignored
----------------------------------

.. code-block:: bash
   :name: test_should_be_ignored

   echo "Not Python → skipped"

Custom pytest marks
-------------------
.. pytestmark: django_db
.. code-block:: python
    :name: test_django

    from django.contrib.auth.models import User

    user = User.objects.first()
