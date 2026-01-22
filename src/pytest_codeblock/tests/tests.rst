Tests
=====

test_group_snippets_merges_named
--------------------------------

.. code-block:: python
    :name: test_group_snippets_merges_named

    import pytest
    from pathlib import Path

    from pytest_codeblock.collector import CodeSnippet, group_snippets
    from pytest_codeblock.md import parse_markdown
    from pytest_codeblock.rst import (
        parse_rst,
        resolve_literalinclude_path,
        get_literalinclude_content,
    )

    # Two snippets with the same name should be combined
    sn1 = CodeSnippet(name="foo", code="a=1", line=1, marks=["codeblock"])
    sn2 = CodeSnippet(name="foo", code="b=2", line=2, marks=["codeblock", "m"])
    combined = group_snippets([sn1, sn2])
    assert len(combined) == 1
    cs = combined[0]
    assert cs.name == "foo"
    # Both code parts should appear
    assert "a=1" in cs.code
    assert "b=2" in cs.code
    # Marks should accumulate
    assert "m" in cs.marks

----

test_group_snippets_different_names
-----------------------------------

.. code-block:: python
    :name: test_group_snippets_different_names

    import pytest
    from pathlib import Path

    from pytest_codeblock.collector import CodeSnippet, group_snippets
    from pytest_codeblock.md import parse_markdown
    from pytest_codeblock.rst import (
        parse_rst,
        resolve_literalinclude_path,
        get_literalinclude_content,
    )

    # Snippets with different names are not grouped
    sn1 = CodeSnippet(name="foo", code="x=1", line=1)
    sn2 = CodeSnippet(name="bar", code="y=2", line=2)
    combined = group_snippets([sn1, sn2])
    assert len(combined) == 2
    assert combined[0].name.startswith("foo")
    assert combined[1].name.startswith("bar")

----

test_parse_markdown_simple
--------------------------

.. code-block:: python
    :name: test_parse_markdown_simple

    import pytest
    from pathlib import Path

    from pytest_codeblock.collector import CodeSnippet, group_snippets
    from pytest_codeblock.md import parse_markdown
    from pytest_codeblock.rst import (
        parse_rst,
        resolve_literalinclude_path,
        get_literalinclude_content,
    )

    text = """
    ```python name=test_example
    x=1
    assert x==1
    ```"""
    snippets = parse_markdown(text)
    assert len(snippets) == 1
    sn = snippets[0]
    assert sn.name == "test_example"
    assert "x=1" in sn.code

----

test_parse_markdown_with_pytestmark
-----------------------------------

.. code-block:: python
    :name: test_parse_markdown_with_pytestmark

    import pytest
    from pathlib import Path

    from pytest_codeblock.collector import CodeSnippet, group_snippets
    from pytest_codeblock.md import parse_markdown
    from pytest_codeblock.rst import (
        parse_rst,
        resolve_literalinclude_path,
        get_literalinclude_content,
    )

    text = """
    <!-- pytestmark: django_db -->
    ```python name=test_db
    from django.db import models
    ```"""
    snippets = parse_markdown(text)
    assert len(snippets) == 1
    sn = snippets[0]
    # Should include both default and django_db marks
    assert "django_db" in sn.marks
    assert "codeblock" in sn.marks

----

test_pytest_fixtures
--------------------

.. pytestfixture: tmp_path
.. pytestfixture: http_request
.. code-block:: python
    :name: test_pytest_fixtures_1

    d = tmp_path / "sub"
    d.mkdir()  # Create the directory
    assert d.is_dir()  # Verify it was created and is a directory

    assert isinstance(http_request.GET, dict)

----

.. pytestfixture: tmp_path
.. pytestfixture: http_request
.. code-block:: python
    :name: test_pytest_fixtures_2

    d = tmp_path / "sub"
    d.mkdir()  # Create the directory
    assert d.is_dir()  # Verify it was created and is a directory

    assert isinstance(http_request.GET, dict)

----

.. pytestfixture: tmp_path
.. pytestfixture: http_request
.. code-block:: python
    :name: test_pytest_fixtures_3

    d = tmp_path / "sub"
    d.mkdir()  # Create the directory
    assert d.is_dir()  # Verify it was created and is a directory

    assert isinstance(http_request.GET, dict)

----

test_async_example
------------------

.. code-block:: python
    :name: test_async_example

    import asyncio

    result = await asyncio.sleep(0.1, result=42)
    assert result == 42

----

test_group_snippets
-------------------

.. code-block:: python
    :name: test_group_snippets

    text_2 = "Jude"

Something in between

.. continue: test_group_snippets
.. code-block:: python
    :name: test_group_snippets_part_2

    assert text_2
    print(text_2)
