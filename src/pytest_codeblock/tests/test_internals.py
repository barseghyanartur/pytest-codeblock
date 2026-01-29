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

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"


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
