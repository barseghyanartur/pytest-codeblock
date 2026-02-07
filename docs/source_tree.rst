Project source-tree
===================

Below is the layout of our project (to 10 levels), followed by
the contents of each key file.

.. code-block:: bash
   :caption: Project directory layout

   pytest-codeblock/

   ├── docs
   │   ├── _implement_pytest_hooks.rst
   │   ├── changelog.rst
   │   ├── cheatsheet_markdown.rst
   │   ├── cheatsheet_restructured_text.rst
   │   ├── code_of_conduct.rst
   │   ├── conf.py
   │   ├── conf.py.distrib
   │   ├── contributor_guidelines.rst
   │   ├── customisation.rst
   │   ├── documentation.rst
   │   ├── index.rst
   │   ├── index.rst.distrib
   │   ├── llms.rst
   │   ├── make.bat
   │   ├── Makefile
   │   ├── markdown.rst
   │   ├── package.rst
   │   ├── requirements.txt
   │   ├── restructured_text.rst
   │   ├── security.rst
   │   └── source_tree.rst
   ├── examples
   │   ├── customisation_example
   │   │   ├── pyproject.toml
   │   │   ├── test.md
   │   │   ├── test.md.txt
   │   │   ├── test.rst
   │   │   └── test.rst.txt
   │   ├── md_example
   │   │   ├── async.md
   │   │   ├── customisation.md
   │   │   ├── pytest_fixtures.md
   │   │   └── README.md
   │   ├── python
   │   │   ├── __init__.py
   │   │   ├── basic_example.py
   │   │   ├── create_bucket_example.py
   │   │   ├── create_pdf_file_example.py
   │   │   ├── django_example.py
   │   │   ├── tell_me_a_joke_example.py
   │   │   └── tmp_path_example.py
   │   ├── rst_example
   │   │   ├── __init__.py
   │   │   ├── async.rst
   │   │   ├── customisation.rst
   │   │   ├── django_settings.py
   │   │   ├── pytest_fixtures.rst
   │   │   └── README.rst
   │   ├── __init__.py
   │   └── conftest.py
   ├── scripts
   │   └── generate_project_source_tree.py
   ├── src
   │   └── pytest_codeblock
   │       ├── tests
   │       │   ├── __init__.py
   │       │   ├── conftest.py
   │       │   ├── test_customisation.py
   │       │   ├── test_integration.py
   │       │   ├── test_pytest_codeblock.py
   │       │   ├── tests.md
   │       │   └── tests.rst
   │       ├── __init__.py
   │       ├── collector.py
   │       ├── config.py
   │       ├── constants.py
   │       ├── helpers.py
   │       ├── md.py
   │       └── rst.py

docs/_implement_pytest_hooks.rst
--------------------------------

.. literalinclude:: _implement_pytest_hooks.rst
   :language: rst
   :caption: docs/_implement_pytest_hooks.rst

docs/changelog.rst
------------------

.. literalinclude:: changelog.rst
   :language: rst
   :caption: docs/changelog.rst

docs/cheatsheet_markdown.rst
----------------------------

.. literalinclude:: cheatsheet_markdown.rst
   :language: rst
   :caption: docs/cheatsheet_markdown.rst

docs/cheatsheet_restructured_text.rst
-------------------------------------

.. literalinclude:: cheatsheet_restructured_text.rst
   :language: rst
   :caption: docs/cheatsheet_restructured_text.rst

docs/code_of_conduct.rst
------------------------

.. literalinclude:: code_of_conduct.rst
   :language: rst
   :caption: docs/code_of_conduct.rst

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

docs/customisation.rst
----------------------

.. literalinclude:: customisation.rst
   :language: rst
   :caption: docs/customisation.rst

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

docs/markdown.rst
-----------------

.. literalinclude:: markdown.rst
   :language: rst
   :caption: docs/markdown.rst

docs/package.rst
----------------

.. literalinclude:: package.rst
   :language: rst
   :caption: docs/package.rst

docs/restructured_text.rst
--------------------------

.. literalinclude:: restructured_text.rst
   :language: rst
   :caption: docs/restructured_text.rst

docs/security.rst
-----------------

.. literalinclude:: security.rst
   :language: rst
   :caption: docs/security.rst

docs/source_tree.rst
--------------------

.. literalinclude:: source_tree.rst
   :language: rst
   :caption: docs/source_tree.rst

examples/__init__.py
--------------------

.. literalinclude:: ../examples/__init__.py
   :language: python
   :caption: examples/__init__.py

examples/conftest.py
--------------------

.. literalinclude:: ../examples/conftest.py
   :language: python
   :caption: examples/conftest.py

examples/customisation_example/test.md
--------------------------------------

.. literalinclude:: ../examples/customisation_example/test.md
   :language: markdown
   :caption: examples/customisation_example/test.md

examples/customisation_example/test.rst
---------------------------------------

.. literalinclude:: ../examples/customisation_example/test.rst
   :language: rst
   :caption: examples/customisation_example/test.rst

examples/md_example/README.md
-----------------------------

.. literalinclude:: ../examples/md_example/README.md
   :language: markdown
   :caption: examples/md_example/README.md

examples/md_example/async.md
----------------------------

.. literalinclude:: ../examples/md_example/async.md
   :language: markdown
   :caption: examples/md_example/async.md

examples/md_example/customisation.md
------------------------------------

.. literalinclude:: ../examples/md_example/customisation.md
   :language: markdown
   :caption: examples/md_example/customisation.md

examples/md_example/pytest_fixtures.md
--------------------------------------

.. literalinclude:: ../examples/md_example/pytest_fixtures.md
   :language: markdown
   :caption: examples/md_example/pytest_fixtures.md

examples/python/__init__.py
---------------------------

.. literalinclude:: ../examples/python/__init__.py
   :language: python
   :caption: examples/python/__init__.py

examples/python/basic_example.py
--------------------------------

.. literalinclude:: ../examples/python/basic_example.py
   :language: python
   :caption: examples/python/basic_example.py

examples/python/create_bucket_example.py
----------------------------------------

.. literalinclude:: ../examples/python/create_bucket_example.py
   :language: python
   :caption: examples/python/create_bucket_example.py

examples/python/create_pdf_file_example.py
------------------------------------------

.. literalinclude:: ../examples/python/create_pdf_file_example.py
   :language: python
   :caption: examples/python/create_pdf_file_example.py

examples/python/django_example.py
---------------------------------

.. literalinclude:: ../examples/python/django_example.py
   :language: python
   :caption: examples/python/django_example.py

examples/python/tell_me_a_joke_example.py
-----------------------------------------

.. literalinclude:: ../examples/python/tell_me_a_joke_example.py
   :language: python
   :caption: examples/python/tell_me_a_joke_example.py

examples/python/tmp_path_example.py
-----------------------------------

.. literalinclude:: ../examples/python/tmp_path_example.py
   :language: python
   :caption: examples/python/tmp_path_example.py

examples/rst_example/README.rst
-------------------------------

.. literalinclude:: ../examples/rst_example/README.rst
   :language: rst
   :caption: examples/rst_example/README.rst

examples/rst_example/__init__.py
--------------------------------

.. literalinclude:: ../examples/rst_example/__init__.py
   :language: python
   :caption: examples/rst_example/__init__.py

examples/rst_example/async.rst
------------------------------

.. literalinclude:: ../examples/rst_example/async.rst
   :language: rst
   :caption: examples/rst_example/async.rst

examples/rst_example/customisation.rst
--------------------------------------

.. literalinclude:: ../examples/rst_example/customisation.rst
   :language: rst
   :caption: examples/rst_example/customisation.rst

examples/rst_example/django_settings.py
---------------------------------------

.. literalinclude:: ../examples/rst_example/django_settings.py
   :language: python
   :caption: examples/rst_example/django_settings.py

examples/rst_example/pytest_fixtures.rst
----------------------------------------

.. literalinclude:: ../examples/rst_example/pytest_fixtures.rst
   :language: rst
   :caption: examples/rst_example/pytest_fixtures.rst

scripts/generate_project_source_tree.py
---------------------------------------

.. literalinclude:: ../scripts/generate_project_source_tree.py
   :language: python
   :caption: scripts/generate_project_source_tree.py

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

src/pytest_codeblock/tests/conftest.py
--------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/conftest.py
   :language: python
   :caption: src/pytest_codeblock/tests/conftest.py

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

src/pytest_codeblock/tests/test_pytest_codeblock.py
---------------------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/test_pytest_codeblock.py
   :language: python
   :caption: src/pytest_codeblock/tests/test_pytest_codeblock.py

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
