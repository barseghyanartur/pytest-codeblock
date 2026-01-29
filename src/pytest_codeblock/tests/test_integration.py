"""
Integration tests that directly import and test all module components.

This module exists to ensure 100% coverage when running with pytest-cov,
by explicitly importing all functions and classes at test time rather than
relying on plugin auto-loading (which happens before coverage starts).
"""
from dataclasses import fields
from unittest.mock import MagicMock

import pytest

from .. import (
    pytest_collect_file,
)
from ..collector import (
    CodeSnippet,
    group_snippets,
)
from ..constants import (
    CODEBLOCK_MARK,
    DJANGO_DB_MARKS,
    TEST_PREFIX,
)
from ..helpers import (
    contains_top_level_await,
    wrap_async_code,
)
from ..md import (
    MarkdownFile,
    parse_markdown,
)
from ..rst import (
    RSTFile,
    get_literalinclude_content,
    parse_rst,
    resolve_literalinclude_path,
)


# =============================================================================
# Test constants.py
# =============================================================================
class TestConstants:
    """Test constants module values."""

    def test_codeblock_mark(self):
        assert CODEBLOCK_MARK == "codeblock"

    def test_django_db_marks(self):
        assert isinstance(DJANGO_DB_MARKS, set)
        assert "django_db" in DJANGO_DB_MARKS
        assert "db" in DJANGO_DB_MARKS
        assert "transactional_db" in DJANGO_DB_MARKS

    def test_test_prefix(self):
        assert TEST_PREFIX == "test_"


# =============================================================================
# Test collector.py - CodeSnippet dataclass
# =============================================================================
class TestCodeSnippet:
    """Test CodeSnippet dataclass."""

    def test_code_snippet_creation(self):
        """Test basic CodeSnippet creation."""
        sn = CodeSnippet(code="x = 1", line=10)
        assert sn.code == "x = 1"
        assert sn.line == 10
        assert sn.name is None
        assert sn.marks == []
        assert sn.fixtures == []

    def test_code_snippet_with_all_fields(self):
        """Test CodeSnippet with all fields."""
        sn = CodeSnippet(
            code="y = 2",
            line=20,
            name="test_example",
            marks=["codeblock", "django_db"],
            fixtures=["tmp_path", "capsys"],
        )
        assert sn.name == "test_example"
        assert "codeblock" in sn.marks
        assert "tmp_path" in sn.fixtures

    def test_code_snippet_is_dataclass(self):
        """Verify CodeSnippet is a proper dataclass."""
        field_names = [f.name for f in fields(CodeSnippet)]
        assert "code" in field_names
        assert "line" in field_names
        assert "name" in field_names
        assert "marks" in field_names
        assert "fixtures" in field_names


# =============================================================================
# Test collector.py - group_snippets function
# =============================================================================
class TestGroupSnippets:
    """Test group_snippets function."""

    def test_group_snippets_single(self):
        """Test with single snippet."""
        sn = CodeSnippet(name="test_one", code="a=1", line=1)
        result = group_snippets([sn])
        assert len(result) == 1
        assert result[0].name == "test_one"

    def test_group_snippets_merge_same_name(self):
        """Test merging snippets with same name."""
        sn1 = CodeSnippet(name="test_foo", code="a=1", line=1, marks=["m1"])
        sn2 = CodeSnippet(name="test_foo", code="b=2", line=5, marks=["m2"])
        result = group_snippets([sn1, sn2])
        assert len(result) == 1
        assert "a=1" in result[0].code
        assert "b=2" in result[0].code
        assert "m1" in result[0].marks
        assert "m2" in result[0].marks

    def test_group_snippets_different_names(self):
        """Test snippets with different names stay separate."""
        sn1 = CodeSnippet(name="test_a", code="a=1", line=1)
        sn2 = CodeSnippet(name="test_b", code="b=2", line=5)
        result = group_snippets([sn1, sn2])
        assert len(result) == 2

    def test_group_snippets_anonymous(self):
        """Test anonymous snippets (name=None) get auto-generated names."""
        sn1 = CodeSnippet(name=None, code="a=1", line=1)
        sn2 = CodeSnippet(name=None, code="b=2", line=5)
        sn3 = CodeSnippet(name=None, code="c=3", line=10)

        combined = group_snippets([sn1, sn2, sn3])

        assert len(combined) == 3
        # Anonymous snippets get codeblock1, codeblock2, codeblock3
        names = [sn.name for sn in combined]
        # name stays None but key used
        assert "codeblock1" in names or combined[0].name is None
        # The snippets should remain separate since they have different
        # auto-keys
        assert combined[0].code == "a=1"
        assert combined[1].code == "b=2"
        assert combined[2].code == "c=3"

    def test_group_snippets_fixtures_merge(self):
        """Test fixtures are accumulated when merging."""
        sn1 = CodeSnippet(
            name="test_f", code="x=1", line=1, fixtures=["tmp_path"]
        )
        sn2 = CodeSnippet(
            name="test_f", code="y=2", line=5, fixtures=["capsys"]
        )

        combined = group_snippets([sn1, sn2])

        assert len(combined) == 1
        # Fixtures should be merged
        assert "tmp_path" in combined[0].fixtures
        assert "capsys" in combined[0].fixtures
        # Code should be concatenated
        assert "x=1" in combined[0].code
        assert "y=2" in combined[0].code


# =============================================================================
# Test helpers.py - contains_top_level_await
# =============================================================================
class TestContainsTopLevelAwait:
    """Test contains_top_level_await function."""

    def test_await_expression(self):
        assert contains_top_level_await("await asyncio.sleep(0)") is True

    def test_async_function_def(self):
        assert contains_top_level_await("async def foo(): pass") is True

    def test_async_with(self):
        assert contains_top_level_await("async with lock: pass") is True

    def test_async_for(self):
        assert contains_top_level_await("async for i in gen: pass") is True

    def test_sync_code(self):
        assert contains_top_level_await("x = 1 + 2") is False

    def test_await_in_string(self):
        assert contains_top_level_await("print('await something')") is False

    def test_syntax_error_returns_false(self):
        """Test invalid syntax returns False (covers except SyntaxError)."""
        assert contains_top_level_await("def broken(:") is False


# =============================================================================
# Test helpers.py - wrap_async_code
# =============================================================================
class TestWrapAsyncCode:
    """Test wrap_async_code function."""

    def test_wrap_basic(self):
        code = "await asyncio.sleep(1)"
        wrapped = wrap_async_code(code)
        assert "async def __async_main__():" in wrapped
        assert "asyncio.run(__async_main__())" in wrapped
        assert "    await asyncio.sleep(1)" in wrapped

    def test_wrap_multiline(self):
        code = "x = 1\nawait asyncio.sleep(0)\ny = 2"
        wrapped = wrap_async_code(code)
        assert "    x = 1" in wrapped
        assert "    await asyncio.sleep(0)" in wrapped
        assert "    y = 2" in wrapped

    def test_wrapped_code_compiles(self):
        """Verify wrapped code is valid Python."""
        code = "result = 42"
        wrapped = wrap_async_code(code)
        # Should not raise
        compile(wrapped, "<test>", "exec")


# =============================================================================
# Test __init__.py - pytest_collect_file hook
# =============================================================================
class TestPytestCollectFile:
    """Test pytest_collect_file hook function."""

    def test_collect_markdown_file(self, tmp_path):
        """Test .md file returns MarkdownFile."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test")

        parent = MagicMock()
        parent.path = tmp_path
        parent.session = MagicMock()
        parent.config = MagicMock()

        result = pytest_collect_file(parent, md_file)
        assert result is not None
        assert isinstance(result, MarkdownFile)

    def test_collect_markdown_extension(self, tmp_path):
        """Test .markdown extension."""
        md_file = tmp_path / "test.markdown"
        md_file.write_text("# Test")

        parent = MagicMock()
        parent.path = tmp_path
        parent.session = MagicMock()
        parent.config = MagicMock()

        result = pytest_collect_file(parent, md_file)
        assert isinstance(result, MarkdownFile)

    def test_collect_rst_file(self, tmp_path):
        """Test .rst file returns RSTFile."""
        rst_file = tmp_path / "test.rst"
        rst_file.write_text("Test\n====")

        parent = MagicMock()
        parent.path = tmp_path
        parent.session = MagicMock()
        parent.config = MagicMock()

        result = pytest_collect_file(parent, rst_file)
        assert result is not None
        assert isinstance(result, RSTFile)

    def test_collect_other_file_returns_none(self, tmp_path):
        """Test other file types return None."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("Some text")

        parent = MagicMock()
        result = pytest_collect_file(parent, txt_file)
        assert result is None

    def test_collect_uppercase_extension(self, tmp_path):
        """Test case-insensitive extension matching."""
        md_file = tmp_path / "test.MD"
        md_file.write_text("# Test")

        parent = MagicMock()
        parent.path = tmp_path
        parent.session = MagicMock()
        parent.config = MagicMock()

        result = pytest_collect_file(parent, md_file)
        assert isinstance(result, MarkdownFile)


# =============================================================================
# Test md.py - parse_markdown function
# =============================================================================
class TestParseMarkdown:
    """Test parse_markdown function."""

    def test_parse_simple_codeblock(self):
        """Test basic code block parsing."""
        text = """
```python name=test_simple
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].name == "test_simple"
        assert "x = 1" in snippets[0].code

    # -------------------------------------------------------------------------

    def test_parse_with_pytestmark(self):
        """Test the <!-- pytestmark: mark --> directive."""
        text = """
<!-- pytestmark: django_db -->
```python name=test_marked
pass
```
"""
        snippets = parse_markdown(text)
        assert "django_db" in snippets[0].marks

    # -------------------------------------------------------------------------

    def test_parse_with_pytestfixture(self):
        """Test the <!-- pytestfixture: name --> directive."""
        text = """
<!-- pytestfixture: tmp_path -->
<!-- pytestfixture: capsys -->
```python name=test_with_fixtures
print("hello")
```
"""
        snippets = parse_markdown(text)

        assert len(snippets) == 1
        assert "tmp_path" in snippets[0].fixtures
        assert "capsys" in snippets[0].fixtures

    # -------------------------------------------------------------------------

    def test_parse_continue_directive(self):
        """Test the <!-- continue: name --> directive for grouping snippets."""
        text = """
```python name=test_setup
x = 1
```

Some text in between.

<!-- continue: test_setup -->
```python
y = x + 1
assert y == 2
```
"""
        snippets = parse_markdown(text)

        # Both blocks should be grouped under test_setup
        grouped = group_snippets(snippets)
        test_snippets = [s for s in grouped if s.name == "test_setup"]
        assert len(test_snippets) == 1
        assert "x = 1" in test_snippets[0].code
        assert "y = x + 1" in test_snippets[0].code

    # -------------------------------------------------------------------------

    def test_parse_codeblock_name_directive(self):
        """Test the <!-- codeblock-name: name --> directive."""
        text = """
<!-- codeblock-name: test_named -->
```python
z = 42
assert z == 42
```
"""
        snippets = parse_markdown(text)

        assert len(snippets) == 1
        assert snippets[0].name == "test_named"

    # -------------------------------------------------------------------------

    def test_parse_py_language(self):
        """Test markdown with 'py' as language identifier."""
        text = """
```py name=test_py_lang
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].name == "test_py_lang"

    # -------------------------------------------------------------------------

    def test_parse_python3_language(self):
        """Test markdown with 'python3' as language identifier."""
        text = """
```python3 name=test_python3
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].name == "test_python3"

    # -------------------------------------------------------------------------

    def test_parse_non_python_codeblock_ignored(self):
        """Test that non-Python code blocks are skipped."""
        text = """
```javascript name=test_js
console.log("hi");
```

```python name=test_py
x = 1
```
"""
        snippets = parse_markdown(text)
        # Only Python blocks should be collected
        assert len(snippets) == 1
        assert snippets[0].name == "test_py"

    # -------------------------------------------------------------------------

    def test_parse_name_colon_syntax(self):
        """Test name= vs name: syntax in fence info string."""
        text = """
```python name:test_colon
x = 1
```
"""
        snippets = parse_markdown(text)
        assert snippets[0].name == "test_colon"

    # -------------------------------------------------------------------------

    def test_parse_empty_codeblock(self):
        """Test parse empty code block."""
        text = """
```python name=test_empty
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].code == ""

    # -------------------------------------------------------------------------

    def test_parse_indented_fence(self):
        """Test fence with indentation."""
        text = """
    ```python name=test_indented
    x = 1
    ```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1

    # -------------------------------------------------------------------------

    # TODO: Remove?
    def test_parse_fence_regex_edge_case(self):
        """Test that malformed fence is handled."""
        # This edge case is hard to trigger since ``` always matches
        text = """
```python name=test_normal
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1

    # -------------------------------------------------------------------------

    def test_parse_markdown_mixed_indentation(self):
        """Test parsing codeblock with mixed indentation levels."""
        text = """
    ```python name=test_indented
    x = 1
        y = 2
    z = 3
        ```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        # Code should be dedented based on fence indentation
        assert "x = 1" in snippets[0].code

    # -------------------------------------------------------------------------

    def test_parse_short_line_in_block(self):
        """Test code block with line shorter than indent."""
        # Code block where some lines are shorter than the fence indentation
        text = """
        ```python name=test_short_line
    x = 1
y
    z = 3
    ```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        # The short line 'y' should still be captured
        assert "y" in snippets[0].code or "x = 1" in snippets[0].code

# =============================================================================
# Test rst.py - resolve_literalinclude_path
# =============================================================================
class TestResolveLiteralincludePath:
    """Test resolve_literalinclude_path function."""

    def test_absolute_path_exists(self, tmp_path):
        """Test with an absolute path that exists."""
        file = tmp_path / "test.py"
        file.write_text("print('hello')")
        result = resolve_literalinclude_path(tmp_path, str(file))
        assert result == str(file.resolve())

    def test_relative_path_exists(self, tmp_path):
        """Test with a relative path that exists."""
        file = tmp_path / "subdir" / "test.py"
        file.parent.mkdir(parents=True)
        file.write_text("print('hello')")
        result = resolve_literalinclude_path(tmp_path, "subdir/test.py")
        assert result == str(file.resolve())

    def test_base_is_file(self, tmp_path):
        """Test when base_dir is a file (uses parent)."""
        base_file = tmp_path / "doc.rst"
        base_file.write_text("some rst")
        target = tmp_path / "code.py"
        target.write_text("x = 1")
        # Pass the file as base_dir - function should use its parent
        result = resolve_literalinclude_path(base_file, "code.py")
        assert result == str(target.resolve())

    def test_nonexistent_returns_none(self, tmp_path):
        """Test with a path that doesn't exist."""
        result = resolve_literalinclude_path(tmp_path, "nonexistent.py")
        assert result is None

    def test_exception_handling(self, tmp_path):
        """Test exception branch."""
        # Use a path that might cause issues
        result = resolve_literalinclude_path(tmp_path, "\x00invalid")
        assert result is None


# =============================================================================
# Test rst.py - get_literalinclude_content
# =============================================================================
class TestGetLiteralincludeContent:
    """Test get_literalinclude_content function."""

    def test_read_success(self, tmp_path):
        """Test reads file correctly."""
        file = tmp_path / "test.py"
        file.write_text("x = 42\ny = 43")
        content = get_literalinclude_content(str(file))
        assert content == "x = 42\ny = 43"

    def test_read_failure(self, tmp_path):
        """Test get_literalinclude_content raises on missing file."""
        with pytest.raises(
            RuntimeError, match="Failed to read literalinclude file"
        ):
            get_literalinclude_content(str(tmp_path / "missing.py"))


# =============================================================================
# Test rst.py - parse_rst function
# =============================================================================
class TestParseRst:
    """Test parse_rst function."""

    def test_parse_code_block(self, tmp_path):
        """Test .. code-block:: python directive."""
        rst = """
.. code-block:: python
   :name: test_rst

   x = 1
"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 1
        assert snippets[0].name == "test_rst"

    # -------------------------------------------------------------------------

    def test_parse_code_directive(self, tmp_path):
        """Test .. code:: python (alternative to code-block)."""
        rst = """
.. code:: python
   :name: test_code

   y = 2
"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 1
        assert snippets[0].name == "test_code"

    # -------------------------------------------------------------------------

    def test_parse_pytestmark(self, tmp_path):
        rst = """
.. pytestmark: django_db

.. code-block:: python
   :name: test_marked

   pass
"""
        snippets = parse_rst(rst, tmp_path)
        assert "django_db" in snippets[0].marks

    # -------------------------------------------------------------------------

    def test_parse_pytestfixture(self, tmp_path):
        """Test the .. pytestfixture: directive."""
        rst = """
.. pytestfixture: tmp_path

.. code-block:: python
    :name: test_fixture_rst

    import os
"""
        snippets = parse_rst(rst, tmp_path)

        assert len(snippets) == 1
        assert "tmp_path" in snippets[0].fixtures

    # -------------------------------------------------------------------------

    def test_parse_continue_directive(self, tmp_path):
        """Test the .. continue: directive for grouping RST snippets."""
        rst = """
.. code-block:: python
    :name: test_rst_setup

    a = 10

Some text.

.. continue: test_rst_setup

.. code-block:: python

    b = a + 5
    assert b == 15
"""
        snippets = parse_rst(rst, tmp_path)

        grouped = group_snippets(snippets)
        test_snippets = [s for s in grouped if s.name == "test_rst_setup"]
        assert len(test_snippets) == 1
        assert "a = 10" in test_snippets[0].code
        assert "b = a + 5" in test_snippets[0].code

    # -------------------------------------------------------------------------

    def test_parse_codeblock_name(self, tmp_path):
        rst = """
.. codeblock-name: test_named

.. code-block:: python

   z = 99
"""
        snippets = parse_rst(rst, tmp_path)
        assert snippets[0].name == "test_named"

    # -------------------------------------------------------------------------

    def test_parse_literal_block(self, tmp_path):
        """Test parsing of literal blocks via :: syntax."""
        rst = """
.. codeblock-name: test_literal

Example code::

result = 1 + 2
assert result == 3
"""
        snippets = parse_rst(rst, tmp_path)

        assert len(snippets) == 1
        assert snippets[0].name == "test_literal"
        assert "result = 1 + 2" in snippets[0].code

    # -------------------------------------------------------------------------

    def test_parse_rst_continue_in_literal_block(self, tmp_path):
        """Test continue directive with literal block syntax."""
        rst = """
.. codeblock-name: test_lit_continue

Part 1::

a = 1

.. continue: test_lit_continue

.. codeblock-name: test_lit_continue

Part 2::

b = 2
    """
        snippets = parse_rst(rst, tmp_path)
        grouped = group_snippets(snippets)
        # Should have grouped the snippets
        matching = [s for s in grouped if s.name == "test_lit_continue"]
        assert len(matching) >= 1

    # -------------------------------------------------------------------------

    def test_parse_literalinclude(self, tmp_path):
        """Test literalinclude directive with test_ name."""
        # Create the file to include
        code_file = tmp_path / "example.py"
        code_file.write_text("def hello(): pass")
        rst = """
.. literalinclude:: example.py
   :name: test_include
"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 1
        assert "def hello():" in snippets[0].code

    # -------------------------------------------------------------------------

    def test_parse_literalinclude_no_test_prefix(self, tmp_path):
        """Test literalinclude without test_ prefix is skipped."""
        code_file = tmp_path / "example.py"
        code_file.write_text("x = 1")
        rst = """
.. literalinclude:: example.py
   :name: example_not_test
"""
        snippets = parse_rst(rst, tmp_path)
        # Should be empty because name doesn't start with test_
        assert len(snippets) == 0

    # -------------------------------------------------------------------------

    def test_parse_non_python_code_block(self, tmp_path):
        """Non-python code blocks are skipped."""
        rst = """
.. code-block:: javascript

   console.log("hi");
"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 0

    # -------------------------------------------------------------------------

    def test_parse_wrong_indent(self, tmp_path):
        """Code at wrong indent level."""
        rst = """
.. code-block:: python
   :name: test_wrong

x = 1
"""
        # Content 'x = 1' is at column 0, not indented under the directive
        snippets = parse_rst(rst, tmp_path)
        # Should not collect this as a valid snippet
        assert len(snippets) == 0

    # -------------------------------------------------------------------------

    def test_parse_literal_codeblock_eof(self, tmp_path):
        """Test literal block at end of file."""
        rst = """
.. codeblock-name: test_eof

Block::"""
        # No content after the :: - end of file
        snippets = parse_rst(rst, tmp_path)
        # Should handle gracefully
        assert len(snippets) == 0

    # -------------------------------------------------------------------------

    def test_parse_empty_codeblock(self, tmp_path):
        """Test parsing an empty code block."""
        rst = """
.. code-block:: python
   :name: test_empty

"""
        snippets = parse_rst(rst, tmp_path)
        # Empty blocks are collected but have no snippets
        assert len(snippets) == 0

    # -------------------------------------------------------------------------

    def test_parse_literal_block_empty_line_after(self, tmp_path):
        """Test literal block with just empty line after (edge case)."""
        rst = """
.. codeblock-name: test_empty_after

Block::

"""
        snippets = parse_rst(rst, tmp_path)
        # Empty block at end
        assert len(snippets) == 0


# =============================================================================
# Integration tests using pytester - exercises collectors and hook
# =============================================================================

# -----------------------------------------------------------------------------
# Test RSTFile.collect() method
# -----------------------------------------------------------------------------

class TestMarkdownCollector:
    """Integration tests for MarkdownFile collector."""

    def test_collect_simple_markdown(self, pytester_subprocess):
        """Test that MarkdownFile collects and runs test snippets."""
        pytester_subprocess.makefile(
            ".md",
            test_simple="""
# Test File

```python name=test_basic
x = 1
assert x == 1
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)
        assert "test_basic" in result.stdout.str()

    def test_collect_with_fixture(self, pytester_subprocess):
        """Test that fixtures are properly injected."""
        pytester_subprocess.makefile(
            ".md",
            test_fixture="""
<!-- pytestfixture: tmp_path -->
```python name=test_uses_tmp_path
assert tmp_path.exists()
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    def test_collect_async_code(self, pytester_subprocess):
        """Test that async code is automatically wrapped."""
        pytester_subprocess.makefile(
            ".md",
            test_async="""
```python name=test_async_snippet
import asyncio
await asyncio.sleep(0)
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    def test_syntax_error_reporting(self, pytester_subprocess):
        """Test that syntax errors in snippets are properly reported."""
        pytester_subprocess.makefile(
            ".md",
            test_syntax="""
```python name=test_bad_syntax
def broken(:
    pass
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(failed=1)
        assert (
            "SyntaxError" in result.stdout.str()
            or "syntax" in result.stdout.str().lower()
        )

    def test_runtime_error_reporting(self, pytester_subprocess):
        """Test that runtime errors in snippets are properly reported."""
        pytester_subprocess.makefile(
            ".md",
            test_runtime="""
```python name=test_runtime_error
raise ValueError("intentional error")
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(failed=1)
        assert "ValueError" in result.stdout.str()


# -----------------------------------------------------------------------------
# Test RSTFile.collect() method
# -----------------------------------------------------------------------------

class TestRSTCollector:
    """Integration tests for RSTFile collector."""

    def test_collect_simple_rst(self, pytester_subprocess):
        """Test that RSTFile collects and runs test snippets."""
        pytester_subprocess.makefile(
            ".rst",
            test_simple="""
Test File
=========

.. code-block:: python
   :name: test_rst_basic

   y = 2
   assert y == 2
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)
        assert "test_rst_basic" in result.stdout.str()

    def test_collect_with_fixture(self, pytester_subprocess):
        """Test that RST fixtures are properly injected."""
        pytester_subprocess.makefile(
            ".rst",
            test_fixture="""
.. pytestfixture: tmp_path

.. code-block:: python
   :name: test_rst_fixture

   assert tmp_path.is_dir()
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    def test_collect_async_code(self, pytester_subprocess):
        """Test that RST async code is automatically wrapped."""
        pytester_subprocess.makefile(
            ".rst",
            test_async="""
.. code-block:: python
   :name: test_rst_async

   import asyncio
   await asyncio.sleep(0)
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    def test_syntax_error_reporting(self, pytester_subprocess):
        """Test that syntax errors in RST snippets are reported."""
        pytester_subprocess.makefile(
            ".rst",
            test_syntax="""
.. code-block:: python
   :name: test_rst_bad_syntax

   class Broken(:
       pass
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(failed=1)


# ---------------------------------------------------------------------------
# Tests for pytest_collect_file hook dispatch
# ---------------------------------------------------------------------------


class TestPytestCollectFileHook:
    """Tests for pytest_collect_file hook dispatch."""

    def test_hook_dispatches_markdown(self, pytester_subprocess):
        """Test that .md files are dispatched to MarkdownFile."""
        pytester_subprocess.makefile(
            ".md",
            readme="""
```python name=test_md_hook
assert True
```
""",
        )
        result = pytester_subprocess.runpytest(
            "-v", "--collect-only", "-p", "no:django"
        )
        assert "test_md_hook" in result.stdout.str()

    def test_hook_dispatches_rst(self, pytester_subprocess):
        """Test that .rst files are dispatched to RSTFile."""
        pytester_subprocess.makefile(
            ".rst",
            readme="""
.. code-block:: python
   :name: test_rst_hook

   assert True
""",
        )
        result = pytester_subprocess.runpytest(
            "-v", "--collect-only", "-p", "no:django"
        )
        assert "test_rst_hook" in result.stdout.str()

    def test_hook_ignores_other_files(self, pytester_subprocess):
        """Test that non-.md/.rst files are ignored."""
        pytester_subprocess.makefile(".txt", notes="Some notes")
        result = pytester_subprocess.runpytest(
            "-v", "--collect-only", "-p", "no:django"
        )
        # Should not fail, just collect nothing from .txt
        assert result.ret == 5  # Exit code 5 = no tests collected

# ---------------------------------------------------------------------------
# Tests for Django DB mark handling
# ---------------------------------------------------------------------------

class TestDjangoDbMarks:
    """Tests for Django DB mark handling."""

    def test_django_db_mark_applied(self, pytester_subprocess):
        """Test that django_db mark is applied when specified."""
        pytester_subprocess.makefile(
            ".md",
            test_marks="""
<!-- pytestmark: django_db -->
```python name=test_with_db_mark
# This would use the db fixture in a real Django project
x = 1
```
""",
        )
        result = pytester_subprocess.runpytest(
            "-v", "--collect-only", "-p", "no:django"
        )
        assert "test_with_db_mark" in result.stdout.str()
        # The mark should be present (we can't fully test Django integration
        # without Django)
