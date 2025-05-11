Project Overview
================

Below is the layout of our project (to 10 levels), followed by the contents of each key file.

.. code-block:: bash
   :caption: Project directory layout

   pytest-codeblock/

   ├── docs
   │   ├── _static
   │   ├── _templates
   │   ├── _implement_pytest_hooks.rst
   │   ├── changelog.rst
   │   ├── code_of_conduct.rst
   │   ├── conf.py
   │   ├── conf.py.distrib
   │   ├── contributor_guidelines.rst
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
   │   └── security.rst
   ├── examples
   │   ├── md_example
   │   │   ├── customisation.md
   │   │   └── README.md
   │   ├── python
   │   │   ├── __init__.py
   │   │   ├── basic_example.py
   │   │   ├── create_bucket_example.py
   │   │   ├── create_pdf_file_example.py
   │   │   ├── django_example.py
   │   │   └── tell_me_a_joke_example.py
   │   └── rst_example
   │       ├── __pycache__
   │       ├── __init__.py
   │       ├── customisation.rst
   │       ├── django_settings.py
   │       └── README.rst
   ├── scripts
   │   └── generate_project_source_tree.py
   ├── src
   │   └── pytest_codeblock
   │       ├── __pycache__
   │       ├── tests
   │       │   ├── __pycache__
   │       │   ├── __init__.py
   │       │   ├── test_pytest_codeblock.py
   │       │   └── tests.rst
   │       ├── __init__.py
   │       ├── collector.py
   │       ├── constants.py
   │       ├── md.py
   │       ├── rst.py

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

examples/md_example/README.md
-----------------------------

.. literalinclude:: ../examples/md_example/README.md
   :language: markdown
   :caption: examples/md_example/README.md

examples/md_example/customisation.md
------------------------------------

.. literalinclude:: ../examples/md_example/customisation.md
   :language: markdown
   :caption: examples/md_example/customisation.md

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

src/pytest_codeblock/constants.py
---------------------------------

.. literalinclude:: ../src/pytest_codeblock/constants.py
   :language: python
   :caption: src/pytest_codeblock/constants.py

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

src/pytest_codeblock/tests/test_pytest_codeblock.py
---------------------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/test_pytest_codeblock.py
   :language: python
   :caption: src/pytest_codeblock/tests/test_pytest_codeblock.py

src/pytest_codeblock/tests/tests.rst
------------------------------------

.. literalinclude:: ../src/pytest_codeblock/tests/tests.rst
   :language: rst
   :caption: src/pytest_codeblock/tests/tests.rst
