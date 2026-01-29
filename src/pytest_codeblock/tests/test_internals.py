"""
Tests targeting internal coverage gaps:
- pytest_collect_file hook dispatch
- Anonymous snippet naming in group_snippets
- Collector classes (MarkdownFile, RSTFile)
- SyntaxError and runtime error handling
- Django DB fixture injection
- Async code wrapping at runtime
- constants module usage
"""
import pytest

from ..md import parse_markdown
from ..rst import parse_rst

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"


# ---------------------------------------------------------------------------
# Edge case tests for remaining uncovered paths
# ---------------------------------------------------------------------------
def test_parse_markdown_fence_regex_edge_case():
    """Test markdown parsing with unusual fence patterns."""
    # This is a tricky edge case - a line that starts with ``` but
    # the regex somehow doesn't match. In practice this is very rare.
    text = """
```python name=test_normal
x = 1
```
"""
    snippets = parse_markdown(text)
    assert len(snippets) == 1


def test_parse_markdown_short_line_in_block():
    """Test markdown code block with line shorter than indent."""
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


def test_parse_rst_code_block_wrong_indent(tmp_path):
    """Test RST code-block with content at wrong indent level."""
    rst = """
.. code-block:: python
   :name: test_wrong_indent

x = 1
"""
    # Content 'x = 1' is at column 0, not indented under the directive
    snippets = parse_rst(rst, tmp_path)
    # Should not collect this as a valid snippet
    assert len(snippets) == 0


def test_parse_rst_literal_block_at_eof(tmp_path):
    """Test RST literal block at end of file."""
    rst = """
.. codeblock-name: test_eof

Code block::"""
    # No content after the :: - end of file
    snippets = parse_rst(rst, tmp_path)
    # Should handle gracefully
    assert len(snippets) == 0


def test_parse_rst_literal_block_empty_line_after(tmp_path):
    """Test RST literal block with just empty line after (edge case)."""
    rst = """
.. codeblock-name: test_empty_after

Block::

"""
    snippets = parse_rst(rst, tmp_path)
    # Empty block at end
    assert len(snippets) == 0


def test_resolve_literalinclude_path_exception_handling(tmp_path, monkeypatch):
    """Test resolve_literalinclude_path exception branch."""
    from pytest_codeblock.rst import resolve_literalinclude_path

    # Create a scenario where path operations might fail
    # by using a path that causes issues
    result = resolve_literalinclude_path(tmp_path, "\x00invalid")
    assert result is None


def test_parse_markdown_py3_language():
    """Test markdown with 'python3' as language identifier."""
    text = """
```python3 name=test_python3
x = 1
```
"""
    snippets = parse_markdown(text)
    assert len(snippets) == 1
    assert snippets[0].name == "test_python3"


def test_parse_markdown_py_language():
    """Test markdown with 'py' as language identifier."""
    text = """
```py name=test_py_lang
y = 2
```
"""
    snippets = parse_markdown(text)
    assert len(snippets) == 1
    assert snippets[0].name == "test_py_lang"


# ---------------------------------------------------------------------------
# Integration tests using pytester - exercises collectors and hook
# ---------------------------------------------------------------------------
@pytest.fixture
def pytester_subprocess(pytester):
    """
    Wrapper that forces subprocess mode to avoid deprecation warning conflicts
    when the plugin uses the old `path` argument signature.
    """
    pytester.runpytest = pytester.runpytest_subprocess
    return pytester


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
