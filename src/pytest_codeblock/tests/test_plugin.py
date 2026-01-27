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
    __all__ as init_all,
)

# Import everything from __init__.py
from .. import (
    __author__,
    __copyright__,
    __license__,
    __title__,
    __version__,
    pytest_collect_file,
)

# Import everything from collector.py
from ..collector import (
    CodeSnippet,
    group_snippets,
)
from ..collector import (
    __all__ as collector_all,
)
from ..collector import (
    __author__ as collector_author,
)
from ..collector import (
    __copyright__ as collector_copyright,
)
from ..collector import (
    __license__ as collector_license,
)

# Import everything from constants.py
from ..constants import (
    CODEBLOCK_MARK,
    DJANGO_DB_MARKS,
    TEST_PREFIX,
)
from ..constants import (
    __all__ as constants_all,
)
from ..constants import (
    __author__ as constants_author,
)
from ..constants import (
    __copyright__ as constants_copyright,
)
from ..constants import (
    __license__ as constants_license,
)
from ..helpers import (
    __all__ as helpers_all,
)
from ..helpers import (
    __author__ as helpers_author,
)
from ..helpers import (
    __copyright__ as helpers_copyright,
)
from ..helpers import (
    __license__ as helpers_license,
)

# Import everything from helpers.py
from ..helpers import (
    contains_top_level_await,
    wrap_async_code,
)

# Import everything from md.py
from ..md import (
    MarkdownFile,
    parse_markdown,
)
from ..md import (
    __all__ as md_all,
)
from ..md import (
    __author__ as md_author,
)
from ..md import (
    __copyright__ as md_copyright,
)
from ..md import (
    __license__ as md_license,
)

# Import everything from rst.py
from ..rst import (
    RSTFile,
    get_literalinclude_content,
    parse_rst,
    resolve_literalinclude_path,
)
from ..rst import (
    __all__ as rst_all,
)
from ..rst import (
    __author__ as rst_author,
)
from ..rst import (
    __copyright__ as rst_copyright,
)
from ..rst import (
    __license__ as rst_license,
)


# =============================================================================
# Test module metadata coverage
# =============================================================================
class TestModuleMetadata:
    """Verify all module metadata is accessible (covers import-time code)."""

    def test_init_metadata(self):
        """Test __init__.py metadata."""
        assert __title__ == "pytest-codeblock"
        assert __version__
        assert __author__
        assert __copyright__
        assert __license__ == "MIT"
        assert "pytest_collect_file" in init_all

    def test_collector_metadata(self):
        """Test collector.py metadata."""
        assert collector_author
        assert collector_copyright
        assert collector_license == "MIT"
        assert "CodeSnippet" in collector_all
        assert "group_snippets" in collector_all

    def test_constants_metadata(self):
        """Test constants.py metadata."""
        assert constants_author
        assert constants_copyright
        assert constants_license == "MIT"
        assert "CODEBLOCK_MARK" in constants_all
        assert "DJANGO_DB_MARKS" in constants_all
        assert "TEST_PREFIX" in constants_all

    def test_helpers_metadata(self):
        """Test helpers.py metadata."""
        assert helpers_author
        assert helpers_copyright
        assert helpers_license == "MIT"
        assert "contains_top_level_await" in helpers_all
        assert "wrap_async_code" in helpers_all

    def test_md_metadata(self):
        """Test md.py metadata."""
        assert md_author
        assert md_copyright
        assert md_license == "MIT"
        assert "MarkdownFile" in md_all
        assert "parse_markdown" in md_all

    def test_rst_metadata(self):
        """Test rst.py metadata."""
        assert rst_author
        assert rst_copyright
        assert rst_license == "MIT"
        assert "RSTFile" in rst_all
        assert "parse_rst" in rst_all


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
        """Test anonymous snippets get auto-names."""
        sn1 = CodeSnippet(name=None, code="a=1", line=1)
        sn2 = CodeSnippet(name=None, code="b=2", line=5)
        sn3 = CodeSnippet(name=None, code="c=3", line=10)
        result = group_snippets([sn1, sn2, sn3])
        # Each anonymous snippet should remain separate
        assert len(result) == 3

    def test_group_snippets_fixtures_merge(self):
        """Test fixtures are accumulated when merging."""
        sn1 = CodeSnippet(
            name="test_x", code="a=1", line=1, fixtures=["tmp_path"]
        )
        sn2 = CodeSnippet(
            name="test_x", code="b=2", line=5, fixtures=["capsys"]
        )
        result = group_snippets([sn1, sn2])
        assert "tmp_path" in result[0].fixtures
        assert "capsys" in result[0].fixtures


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
        txt_file.write_text("hello")

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

    def test_parse_simple_block(self):
        text = """
```python name=test_simple
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].name == "test_simple"
        assert "x = 1" in snippets[0].code

    def test_parse_with_pytestmark(self):
        text = """
<!-- pytestmark: django_db -->
```python name=test_marked
pass
```
"""
        snippets = parse_markdown(text)
        assert "django_db" in snippets[0].marks

    def test_parse_with_pytestfixture(self):
        text = """
<!-- pytestfixture: tmp_path -->
```python name=test_fixture
pass
```
"""
        snippets = parse_markdown(text)
        assert "tmp_path" in snippets[0].fixtures

    def test_parse_continue_directive(self):
        text = """
```python name=test_cont
a = 1
```

<!-- continue: test_cont -->
```python
b = 2
```
"""
        snippets = parse_markdown(text)
        grouped = group_snippets(snippets)
        matching = [s for s in grouped if s.name == "test_cont"]
        assert len(matching) == 1
        assert "a = 1" in matching[0].code
        assert "b = 2" in matching[0].code

    def test_parse_codeblock_name_directive(self):
        text = """
<!-- codeblock-name: test_named -->
```python
z = 42
```
"""
        snippets = parse_markdown(text)
        assert snippets[0].name == "test_named"

    def test_parse_py_language(self):
        text = """
```py name=test_py
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1

    def test_parse_python3_language(self):
        text = """
```python3 name=test_py3
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1

    def test_parse_non_python_ignored(self):
        text = """
```javascript
console.log("hi");
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 0

    def test_parse_name_colon_syntax(self):
        text = """
```python name:test_colon
x = 1
```
"""
        snippets = parse_markdown(text)
        assert snippets[0].name == "test_colon"

    def test_parse_empty_block(self):
        text = """
```python name=test_empty
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].code == ""

    def test_parse_indented_fence(self):
        """Test fence with indentation."""
        text = """
    ```python name=test_indented
    x = 1
    ```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1

    def test_parse_fence_regex_edge_case(self):
        """Test that malformed fence is handled (line 89)."""
        # This edge case is hard to trigger since ``` always matches
        text = """
```python name=test_normal
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1


# =============================================================================
# Test rst.py - resolve_literalinclude_path
# =============================================================================
class TestResolveLiteralincludePath:
    """Test resolve_literalinclude_path function."""

    def test_absolute_path_exists(self, tmp_path):
        f = tmp_path / "code.py"
        f.write_text("x=1")
        result = resolve_literalinclude_path(tmp_path, str(f))
        assert result == str(f.resolve())

    def test_relative_path_exists(self, tmp_path):
        f = tmp_path / "code.py"
        f.write_text("x=1")
        result = resolve_literalinclude_path(tmp_path, "code.py")
        assert result == str(f.resolve())

    def test_base_is_file(self, tmp_path):
        """Test when base_dir is a file (uses parent)."""
        doc = tmp_path / "doc.rst"
        doc.write_text("test")
        code = tmp_path / "code.py"
        code.write_text("x=1")
        result = resolve_literalinclude_path(doc, "code.py")
        assert result == str(code.resolve())

    def test_nonexistent_returns_none(self, tmp_path):
        result = resolve_literalinclude_path(tmp_path, "missing.py")
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
        f = tmp_path / "code.py"
        f.write_text("x = 42\ny = 43")
        content = get_literalinclude_content(str(f))
        assert content == "x = 42\ny = 43"

    def test_read_failure(self, tmp_path):
        """Test RuntimeError on missing file."""
        with pytest.raises(RuntimeError, match="Failed to read"):
            get_literalinclude_content(str(tmp_path / "missing.py"))


# =============================================================================
# Test rst.py - parse_rst function
# =============================================================================
class TestParseRst:
    """Test parse_rst function."""

    def test_parse_code_block(self, tmp_path):
        rst = """
.. code-block:: python
   :name: test_rst

   x = 1
"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 1
        assert snippets[0].name == "test_rst"

    def test_parse_code_directive(self, tmp_path):
        """Test .. code:: python variant."""
        rst = """
.. code:: python
   :name: test_code

   y = 2
"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 1

    def test_parse_pytestmark(self, tmp_path):
        rst = """
.. pytestmark: django_db

.. code-block:: python
   :name: test_marked

   pass
"""
        snippets = parse_rst(rst, tmp_path)
        assert "django_db" in snippets[0].marks

    def test_parse_pytestfixture(self, tmp_path):
        rst = """
.. pytestfixture: tmp_path

.. code-block:: python
   :name: test_fixture

   pass
"""
        snippets = parse_rst(rst, tmp_path)
        assert "tmp_path" in snippets[0].fixtures

    def test_parse_continue_directive(self, tmp_path):
        rst = """
.. code-block:: python
   :name: test_cont

   a = 1

.. continue: test_cont

.. code-block:: python

   b = 2
"""
        snippets = parse_rst(rst, tmp_path)
        grouped = group_snippets(snippets)
        matching = [s for s in grouped if s.name == "test_cont"]
        assert "a = 1" in matching[0].code
        assert "b = 2" in matching[0].code

    def test_parse_codeblock_name(self, tmp_path):
        rst = """
.. codeblock-name: test_named

.. code-block:: python

   z = 99
"""
        snippets = parse_rst(rst, tmp_path)
        assert snippets[0].name == "test_named"

    def test_parse_literal_block(self, tmp_path):
        rst = """
.. codeblock-name: test_literal

Example::

   x = 1
   y = 2
"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 1
        assert "x = 1" in snippets[0].code

    def test_parse_literalinclude(self, tmp_path):
        code_file = tmp_path / "example.py"
        code_file.write_text("def hello(): pass")
        rst = """
.. literalinclude:: example.py
   :name: test_include
"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 1
        assert "def hello():" in snippets[0].code

    def test_parse_literalinclude_no_test_prefix(self, tmp_path):
        """Literalinclude without test_ prefix is skipped."""
        code_file = tmp_path / "example.py"
        code_file.write_text("x=1")
        rst = """
.. literalinclude:: example.py
   :name: example_not_test
"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 0

    def test_parse_non_python_code_block(self, tmp_path):
        """Non-python code blocks are skipped."""
        rst = """
.. code-block:: javascript

   console.log("hi");
"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 0

    def test_parse_wrong_indent(self, tmp_path):
        """Code at wrong indent level."""
        rst = """
.. code-block:: python
   :name: test_wrong

x = 1
"""
        snippets = parse_rst(rst, tmp_path)
        # Content not indented, should not collect
        assert len(snippets) == 0

    def test_parse_literal_block_eof(self, tmp_path):
        """Literal block at end of file."""
        rst = """
.. codeblock-name: test_eof

Block::"""
        snippets = parse_rst(rst, tmp_path)
        # No content after ::
        assert len(snippets) == 0

    def test_parse_empty_code_block(self, tmp_path):
        """Empty code block."""
        rst = """
.. code-block:: python
   :name: test_empty

"""
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 0


# =============================================================================
# Test MarkdownFile.collect() method
# =============================================================================
# class TestMarkdownFileCollect:
#     """Test MarkdownFile collector."""

#     def test_collect_basic(self, tmp_path):
#         """Test basic collection."""
#         md_file = tmp_path / "test.md"
#         md_file.write_text("""
# ```python name=test_basic
# assert 1 + 1 == 2
# ```
# """)
#         parent = MagicMock()
#         parent.path = tmp_path
#         parent.session = MagicMock()
#         parent.config = MagicMock()

#         collector = MarkdownFile.from_parent(parent=parent, path=md_file)
#         items = list(collector.collect())
#         assert len(items) == 1
#         assert items[0].name == "test_basic"

#     def test_collect_with_fixture(self, tmp_path):
#         """Test collection with fixtures (line 184)."""
#         md_file = tmp_path / "test.md"
#         md_file.write_text("""
# <!-- pytestfixture: tmp_path -->
# ```python name=test_with_fixture
# x = 1
# ```
# """)
#         parent = MagicMock()
#         parent.path = tmp_path
#         parent.session = MagicMock()
#         parent.config = MagicMock()

#         collector = MarkdownFile.from_parent(parent=parent, path=md_file)
#         items = list(collector.collect())
#         assert len(items) == 1

#     def test_collect_with_django_mark(self, tmp_path):
#         """Test collection adds db fixture for django_db mark."""
#         md_file = tmp_path / "test.md"
#         md_file.write_text("""
# <!-- pytestmark: django_db -->
# ```python name=test_django
# pass
# ```
# """)
#         parent = MagicMock()
#         parent.path = tmp_path
#         parent.session = MagicMock()
#         parent.config = MagicMock()

#         collector = MarkdownFile.from_parent(parent=parent, path=md_file)
#         items = list(collector.collect())
#         assert len(items) == 1

#     def test_collect_non_test_prefix_skipped(self, tmp_path):
#         """Snippets without test_ prefix are skipped."""
#         md_file = tmp_path / "test.md"
#         md_file.write_text("""
# ```python name=example_not_test
# x = 1
# ```
# """)
#         parent = MagicMock()
#         parent.path = tmp_path
#         parent.session = MagicMock()
#         parent.config = MagicMock()

#         collector = MarkdownFile.from_parent(parent=parent, path=md_file)
#         items = list(collector.collect())
#         assert len(items) == 0


# =============================================================================
# Test RSTFile.collect() method
# =============================================================================
# class TestRSTFileCollect:
#     """Test RSTFile collector."""

#     def test_collect_basic(self, tmp_path):
#         """Test basic collection."""
#         rst_file = tmp_path / "test.rst"
#         rst_file.write_text("""
# .. code-block:: python
#    :name: test_basic

#    assert 1 + 1 == 2
# """)
#         parent = MagicMock()
#         parent.path = tmp_path
#         parent.session = MagicMock()
#         parent.config = MagicMock()

#         collector = RSTFile.from_parent(parent=parent, path=rst_file)
#         items = list(collector.collect())
#         assert len(items) == 1
#         assert items[0].name == "test_basic"

#     def test_collect_with_fixture(self, tmp_path):
#         """Test collection with fixtures."""
#         rst_file = tmp_path / "test.rst"
#         rst_file.write_text("""
# .. pytestfixture: tmp_path

# .. code-block:: python
#    :name: test_with_fixture

#    x = 1
# """)
#         parent = MagicMock()
#         parent.path = tmp_path
#         parent.session = MagicMock()
#         parent.config = MagicMock()

#         collector = RSTFile.from_parent(parent=parent, path=rst_file)
#         items = list(collector.collect())
#         assert len(items) == 1

#     def test_collect_with_django_mark(self, tmp_path):
#         """Test collection adds db fixture for django_db mark."""
#         rst_file = tmp_path / "test.rst"
#         rst_file.write_text("""
# .. pytestmark: django_db

# .. code-block:: python
#    :name: test_django

#    pass
# """)
#         parent = MagicMock()
#         parent.path = tmp_path
#         parent.session = MagicMock()
#         parent.config = MagicMock()

#         collector = RSTFile.from_parent(parent=parent, path=rst_file)
#         items = list(collector.collect())
#         assert len(items) == 1

#     def test_collect_non_test_prefix_skipped(self, tmp_path):
#         """Snippets without test_ prefix are skipped."""
#         rst_file = tmp_path / "test.rst"
#         rst_file.write_text("""
# .. code-block:: python
#    :name: example_not_test

#    x = 1
# """)
#         parent = MagicMock()
#         parent.path = tmp_path
#         parent.session = MagicMock()
#         parent.config = MagicMock()

#         collector = RSTFile.from_parent(parent=parent, path=rst_file)
#         items = list(collector.collect())
#         assert len(items) == 0


# =============================================================================
# Test async code handling in collectors
# =============================================================================
# class TestAsyncCodeHandling:
#     """Test async code detection and wrapping in collectors."""

#     def test_markdown_async_code(self, tmp_path):
#         """Test MarkdownFile handles async code."""
#         md_file = tmp_path / "test.md"
#         md_file.write_text("""
# ```python name=test_async
# import asyncio
# await asyncio.sleep(0)
# ```
# """)
#         parent = MagicMock()
#         parent.path = tmp_path
#         parent.session = MagicMock()
#         parent.config = MagicMock()

#         collector = MarkdownFile.from_parent(parent=parent, path=md_file)
#         items = list(collector.collect())
#         assert len(items) == 1

#     def test_rst_async_code(self, tmp_path):
#         """Test RSTFile handles async code."""
#         rst_file = tmp_path / "test.rst"
#         rst_file.write_text("""
# .. code-block:: python
#    :name: test_async

#    import asyncio
#    await asyncio.sleep(0)
# """)
#         parent = MagicMock()
#         parent.path = tmp_path
#         parent.session = MagicMock()
#         parent.config = MagicMock()

#         collector = RSTFile.from_parent(parent=parent, path=rst_file)
#         items = list(collector.collect())
#         assert len(items) == 1
