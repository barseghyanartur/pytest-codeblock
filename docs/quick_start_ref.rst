Quick-start reference
=====================

pytest-codeblock collects Python code blocks from ``.rst`` and ``.md``
files and runs them as pytest tests. No configuration is required for
basic use — files are discovered automatically.

--------------

Naming rules
------------

Only blocks whose name starts with ``test_`` are collected by default.
To test all blocks regardless of name, set
``test_nameless_codeblocks = true`` in ``pyproject.toml``.

--------------

RST syntax
----------

.. code:: rst

   .. code-block:: python
      :name: test_my_example

      result = 1 + 1
      assert result == 2

Add a pytest marker (RST)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: rst

   .. pytestmark: skip
   .. code-block:: python
      :name: test_skipped_block

      pass

Request a fixture (RST)
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: rst

   .. pytestfixture: tmp_path
   .. code-block:: python
      :name: test_uses_tmp_path

      d = tmp_path / "sub"
      d.mkdir()
      assert d.is_dir()

Group blocks (RST) — shared context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: rst

   .. code-block:: python
      :name: test_part_one

      x = 1

   Some prose in between.

   .. continue: test_part_one
   .. code-block:: python
      :name: test_part_two

      y = x + 1
      assert y == 2

All blocks sharing the same group key are concatenated into one test
under the first name.

Incremental grouping — each step is its own test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When every continuation block has a **distinct** name, each step becomes
a cumulative test:

.. code:: rst

   .. code-block:: python
      :name: test_step_1

      a = 1

   .. continue: test_step_1
   .. code-block:: python
      :name: test_step_2

      b = a + 1
      assert b == 2

This produces two tests: ``test_step_1`` (code: ``a=1``) and
``test_step_2`` (code: ``a=1\nb=a+1\nassert b==2``).

Literal block (RST)
~~~~~~~~~~~~~~~~~~~

.. code:: rst

   .. codeblock-name: test_literal_block

   Example code::

      result = "hello"
      assert result == "hello"

Include external file (RST)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: rst

   .. literalinclude:: examples/snippet.py
      :name: test_external_snippet

Run as standalone pytest suite (RST)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: rst

   .. pytestmark: pytestrun
   .. code-block:: python
      :name: test_pytest_style

      import pytest

      class TestMath:
          def test_add(self):
              assert 1 + 1 == 2

--------------

Markdown syntax
---------------

.. code:: markdown

   ```python name=test_my_example
   result = 1 + 1
   assert result == 2
   ```

Add a pytest marker (Markdown)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: markdown

   <!-- pytestmark: skip -->
   ```python name=test_skipped
   pass
   ```

Request a fixture (Markdown)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: markdown

   <!-- pytestfixture: tmp_path -->
   ```python name=test_uses_tmp_path
   d = tmp_path / "sub"
   d.mkdir()
   assert d.is_dir()
   ```

Group blocks (Markdown)
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: markdown

   ```python name=test_setup
   x = 1
   ```

   <!-- continue: test_setup -->
   ```python name=test_continuation
   y = x + 1
   assert y == 2
   ```

Run as standalone pytest suite (Markdown)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: markdown

   <!-- pytestmark: pytestrun -->
   ```python name=test_class_example
   import pytest

   class TestMath:
       @pytest.fixture
       def value(self):
           return 42

       def test_value(self, value):
           assert value == 42
   ```

--------------

Async support
-------------

Top-level ``await`` is automatically wrapped — no extra config needed:

.. code:: rst

   .. code-block:: python
      :name: test_async_block

      import asyncio
      result = await asyncio.sleep(0.1, result=99)
      assert result == 99

--------------

pyproject.toml configuration
----------------------------

.. code:: toml

   [tool.pytest-codeblock]
   # Test all blocks regardless of test_ prefix (default: false)
   test_nameless_codeblocks = false

   # Add custom language identifiers (in addition to python, py, python3)
   rst_user_codeblocks = []
   md_user_codeblocks = []

   # Add custom file extensions
   rst_user_extensions = []
   md_user_extensions = []

testpaths troubleshooting
-------------------------

If docs are not discovered, add explicitly:

.. code:: toml

   [tool.pytest.ini_options]
   testpaths = ["src/app/tests", "docs"]

--------------

conftest.py hook integration
----------------------------

Use ``CODEBLOCK_MARK`` from ``pytest_codeblock.constants`` to identify
doc-block tests:

.. code:: python

   from pytest_codeblock.constants import CODEBLOCK_MARK

   def pytest_collection_modifyitems(config, items):
       for item in items:
           if item.get_closest_marker(CODEBLOCK_MARK):
               item.add_marker(pytest.mark.documentation)

Custom fixtures used in doc blocks are defined in ``conftest.py``
exactly like regular fixtures. Multiple ``pytestfixture`` directives on
consecutive lines are all applied to the next block. Fixture requests in
the first block of a group automatically apply to all continuation
blocks.
