Project source-tree
===================

Below is the layout of the project (to 10 levels), followed by
the contents of each key file.

.. code-block:: text
   :caption: Project directory layout

   pytest-codeblock/
   ├── docs
   │   ├── cheatsheet_markdown.rst
   │   ├── cheatsheet_restructured_text.rst
   │   ├── conf.py
   │   ├── contributor_guidelines.rst
   │   ├── customisation.rst
   │   ├── documentation.rst
   │   ├── full-llms.txt
   │   ├── index.rst
   │   ├── llms.rst
   │   ├── markdown.rst
   │   ├── package.rst
   │   ├── quick_start_ref.rst
   │   ├── requirements.txt
   │   └── restructured_text.rst
   ├── src
   │   └── pytest_codeblock
   │       ├── tests
   │       │   ├── __init__.py
   │       │   ├── test_customisation.py
   │       │   ├── test_integration.py
   │       │   ├── test_nameless_codeblocks.py
   │       │   ├── test_pytest_codeblock.py
   │       │   ├── test_pytestrun_marker.py
   │       │   ├── tests.md
   │       │   └── tests.rst
   │       ├── __init__.py
   │       ├── collector.py
   │       ├── config.py
   │       ├── constants.py
   │       ├── helpers.py
   │       ├── md.py
   │       ├── pytestrun.py
   │       └── rst.py
   ├── conftest.py
   ├── CONTRIBUTING.rst
   ├── Makefile
   ├── pyproject.toml
   └── README.rst

README.rst
----------

.. literalinclude:: ../README.rst
   :language: rst
   :caption: README.rst

CONTRIBUTING.rst
----------------

.. literalinclude:: ../CONTRIBUTING.rst
   :language: rst
   :caption: CONTRIBUTING.rst

docs/quick_start_ref.rst
------------------------

.. literalinclude:: quick_start_ref.rst
   :language: rst
   :caption: docs/quick_start_ref.rst

docs/restructured_text.rst
--------------------------

.. literalinclude:: restructured_text.rst
   :language: rst
   :caption: docs/restructured_text.rst

docs/markdown.rst
-----------------

.. literalinclude:: markdown.rst
   :language: rst
   :caption: docs/markdown.rst

docs/cheatsheet_restructured_text.rst
-------------------------------------

.. literalinclude:: cheatsheet_restructured_text.rst
   :language: rst
   :caption: docs/cheatsheet_restructured_text.rst

docs/cheatsheet_markdown.rst
----------------------------

.. literalinclude:: cheatsheet_markdown.rst
   :language: rst
   :caption: docs/cheatsheet_markdown.rst

docs/customisation.rst
----------------------

.. literalinclude:: customisation.rst
   :language: rst
   :caption: docs/customisation.rst

conftest.py
-----------

.. literalinclude:: ../conftest.py
   :language: python
   :caption: conftest.py

docs/conf.py
------------

.. literalinclude:: conf.py
   :language: python
   :caption: docs/conf.py

docs/contributor_guidelines.rst
-------------------------------

.. literalinclude:: contributor_guidelines.rst
   :language: rst
   :caption: docs/contributor_guidelines.rst

docs/documentation.rst
----------------------

.. literalinclude:: documentation.rst
   :language: rst
   :caption: docs/documentation.rst

docs/index.rst
--------------

.. literalinclude:: index.rst
   :language: rst
   :caption: docs/index.rst

docs/llms.rst
-------------

.. literalinclude:: llms.rst
   :language: rst
   :caption: docs/llms.rst

docs/package.rst
----------------

.. literalinclude:: package.rst
   :language: rst
   :caption: docs/package.rst

pyproject.toml
--------------

.. literalinclude:: ../pyproject.toml
   :language: toml
   :caption: pyproject.toml

src/pytest_codeblock/__init__.py
--------------------------------

.. literalinclude:: ../src/pytest_codeblock/__init__.py
   :language: python
   :caption: src/pytest_codeblock/__init__.py

src/pytest_codeblock/collector.py
---------------------------------

.. literalinclude:: ../src/pytest_codeblock/collector.py
   :language: python
   :caption: src/pytest_codeblock/collector.py

src/pytest_codeblock/config.py
------------------------------

.. literalinclude:: ../src/pytest_codeblock/config.py
   :language: python
   :caption: src/pytest_codeblock/config.py

src/pytest_codeblock/constants.py
---------------------------------

.. literalinclude:: ../src/pytest_codeblock/constants.py
   :language: python
   :caption: src/pytest_codeblock/constants.py

src/pytest_codeblock/helpers.py
-------------------------------

.. literalinclude:: ../src/pytest_codeblock/helpers.py
   :language: python
   :caption: src/pytest_codeblock/helpers.py

src/pytest_codeblock/md.py
--------------------------

.. literalinclude:: ../src/pytest_codeblock/md.py
   :language: python
   :caption: src/pytest_codeblock/md.py

src/pytest_codeblock/pytestrun.py
---------------------------------

.. literalinclude:: ../src/pytest_codeblock/pytestrun.py
   :language: python
   :caption: src/pytest_codeblock/pytestrun.py

src/pytest_codeblock/rst.py
---------------------------

.. literalinclude:: ../src/pytest_codeblock/rst.py
   :language: python
   :caption: src/pytest_codeblock/rst.py

src/pytest_codeblock/tests/__init__.py
--------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/__init__.py
   :language: python
   :caption: src/pytest_codeblock/tests/__init__.py

src/pytest_codeblock/tests/test_customisation.py
------------------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/test_customisation.py
   :language: python
   :caption: src/pytest_codeblock/tests/test_customisation.py

src/pytest_codeblock/tests/test_integration.py
----------------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/test_integration.py
   :language: python
   :caption: src/pytest_codeblock/tests/test_integration.py

src/pytest_codeblock/tests/test_nameless_codeblocks.py
------------------------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/test_nameless_codeblocks.py
   :language: python
   :caption: src/pytest_codeblock/tests/test_nameless_codeblocks.py

src/pytest_codeblock/tests/test_pytest_codeblock.py
---------------------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/test_pytest_codeblock.py
   :language: python
   :caption: src/pytest_codeblock/tests/test_pytest_codeblock.py

src/pytest_codeblock/tests/test_pytestrun_marker.py
---------------------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/test_pytestrun_marker.py
   :language: python
   :caption: src/pytest_codeblock/tests/test_pytestrun_marker.py

src/pytest_codeblock/tests/tests.md
-----------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/tests.md
   :language: markdown
   :caption: src/pytest_codeblock/tests/tests.md

src/pytest_codeblock/tests/tests.rst
------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/tests.rst
   :language: rst
   :caption: src/pytest_codeblock/tests/tests.rst
