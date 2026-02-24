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

----

test_pytestrun_marker
---------------------

.. pytestmark: pytestrun
.. code-block:: python
    :name: test_pytestrun_marker

    import pytest

    class TestSystemInfo:

        @pytest.fixture
        def system_name(self):
            return "Linux"

        @pytest.fixture
        def version_number(self):
            return 5

        def test_combined_info(self, system_name, version_number):
            info = f"{system_name} v{version_number}"
            assert info == "Linux v5"

        def test_name_only(self, system_name):
            assert system_name.isalpha()

----

test_pytestrun_marker_and_conftest_fixtures
-------------------------------------------

.. pytestmark: pytestrun
.. code-block:: python
    :name: test_pytestrun_marker_and_conftest_fixtures

    import pytest

    class TestSystemInfo:

        def test_request(self, http_request):
            assert isinstance(http_request.GET, dict)

----

test_pytestrun_with_setup_teardown
----------------------------------

.. pytestmark: pytestrun
.. code-block:: python
    :name: test_pytestrun_with_setup_teardown

    import pytest

    class TestWithSetup:

        def setup_method(self):
            self.value = 10

        def test_value_set(self):
            assert self.value == 10

        def test_value_modified(self):
            self.value += 5
            assert self.value == 15

----

test_pytestrun_with_parametrize
-------------------------------

.. pytestmark: pytestrun
.. code-block:: python
    :name: test_pytestrun_with_parametrize

    import pytest

    class TestParametrized:

        @pytest.mark.parametrize("input,expected", [(1, 2), (3, 4)])
        def test_increment(self, input, expected):
            assert input + 1 == expected

----

test_pytestrun_nested_fixtures
------------------------------

.. pytestmark: pytestrun
.. code-block:: python
    :name: test_pytestrun_nested_fixtures

    import pytest

    class TestNestedFixtures:

        @pytest.fixture
        def base_value(self):
            return 100

        @pytest.fixture
        def derived_value(self, base_value):
            return base_value * 2

        def test_derived(self, derived_value):
            assert derived_value == 200

----

test_pytestrun_with_conftest_and_class_fixtures
-----------------------------------------------

.. pytestmark: pytestrun
.. code-block:: python
    :name: test_pytestrun_with_conftest_and_class_fixtures

    import pytest

    class TestMixedFixtures:

        @pytest.fixture
        def local_data(self):
            return {"key": "value"}

        def test_both_fixtures(self, http_request, local_data):
            assert isinstance(http_request.GET, dict)
            assert local_data["key"] == "value"

----

test_pytestrun_multiple_test_methods
------------------------------------

.. pytestmark: pytestrun
.. code-block:: python
    :name: test_pytestrun_multiple_test_methods

    import pytest

    class TestMultipleMethods:

        @pytest.fixture
        def shared_list(self):
            return [1, 2, 3]

        def test_length(self, shared_list):
            assert len(shared_list) == 3

        def test_first_element(self, shared_list):
            assert shared_list[0] == 1

        def test_sum(self, shared_list):
            assert sum(shared_list) == 6

----

test_pytestrun_multiple_test_methods_multiple_markers
-----------------------------------------------------

.. pytestmark: pytestrun
.. code-block:: python
    :name: test_pytestrun_multiple_test_methods_multiple_markers

    import pytest

    class TestMultipleMethodsMultipleMarkers:

        @pytest.fixture
        def letter_a(self):
            return "a"

        def test_class_level_fixture(self, letter_a):
            assert letter_a == "a"

        def test_pytest_built_in_fixture(self, tmp_path):
            d = tmp_path / "sub"
            d.mkdir()  # Create the directory
            assert d.is_dir()  # Verify it was created and is a directory

        def test_pytest_user_defined_fixture(self, http_request):
            assert isinstance(http_request.GET, dict)

----

test_updated_grouping
---------------------

.. code-block:: python
    :name: test_updated_grouping

    names = ["Jude"]
    assert len(names) == 1
    print(names)

Something in between

.. continue: test_updated_grouping
.. code-block:: python
    :name: test_updated_grouping_part_2

    assert names
    print(names)
    names.append("Lora")
    assert len(names) == 2

Something in between

.. continue: test_updated_grouping
.. code-block:: python
    :name: test_updated_grouping_part_3

    assert names
    print(names)
    names.append("Alice")
    assert len(names) == 3

----

test_updated_grouping_pytestrun_marker
--------------------------------------

.. pytestmark: pytestrun
.. code-block:: python
    :name: test_updated_grouping_pytestrun_marker

    import pytest

    class TestSample:

        @pytest.fixture
        def system_name(self):
            return "Linux"

        @pytest.fixture
        def version_number(self):
            return 5

        def test_combined_info(self, system_name, version_number):
            info = f"{system_name} v{version_number}"
            assert info == "Linux v5"
            print(info)

Some text in between

.. continue: test_updated_grouping_pytestrun_marker
.. pytestmark: pytestrun
.. code-block:: python
    :name: test_updated_grouping_pytestrun_marker_part_2

    class TestSample:

        @pytest.fixture
        def system_name(self):
            return "macOS"

        @pytest.fixture
        def version_number(self):
            return 17

        def test_combined_info(self, system_name, version_number):
            info = f"{system_name} v{version_number}"
            assert info == "macOS v17"
            print(info)
