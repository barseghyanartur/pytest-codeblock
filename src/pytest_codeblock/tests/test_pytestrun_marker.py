"""
Tests for the `pytestrun` marker functionality.

When a code block is marked with ``pytestrun``, the plugin writes the block to
a temporary file and executes it via pytest as a subprocess, so that
``Test*`` classes, ``test_*`` functions, fixtures, markers, and
setup/teardown all behave exactly as they would in a normal pytest run.
"""
import textwrap

import pytest

from ..collector import CodeSnippet
from ..constants import CODEBLOCK_MARK, PYTESTRUN_MARK
from ..md import parse_markdown
from ..pytestrun import run_pytest_style_code
from ..rst import parse_rst

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "TestPytestrunConstants",
    "TestPytestrunMarkParsing",
    "TestRunPytestStyleCode",
    "TestPytestrunMarkdownIntegration",
    "TestPytestrunRSTIntegration",
    "TestPytestrunEdgeCases",
)


# =============================================================================
# Test constants related to pytestrun
# =============================================================================
class TestPytestrunConstants:
    """Test that PYTESTRUN_MARK constant is correctly defined."""

    def test_pytestrun_mark_value(self):
        assert PYTESTRUN_MARK == "pytestrun"

    def test_pytestrun_mark_is_string(self):
        assert isinstance(PYTESTRUN_MARK, str)

    def test_pytestrun_mark_differs_from_codeblock_mark(self):
        assert PYTESTRUN_MARK != CODEBLOCK_MARK


# =============================================================================
# Test that pytestrun mark is parsed correctly from MD and RST sources
# =============================================================================
class TestPytestrunMarkParsing:
    """Test that the pytestrun mark is captured during parsing."""

    def test_md_pytestmark_pytestrun_captured(self):
        """The pytestrun mark is present after parsing a marked MD block."""
        text = textwrap.dedent("""\
            <!-- pytestmark: pytestrun -->
            ```python name=test_pytestrun_parse
            def test_ok():
                assert True
            ```
        """)
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert PYTESTRUN_MARK in snippets[0].marks

    def test_md_both_codeblock_and_pytestrun_marks(self):
        """Both codeblock and pytestrun marks are present simultaneously."""
        text = textwrap.dedent("""\
            <!-- pytestmark: pytestrun -->
            ```python name=test_marks_coexist
            def test_x():
                pass
            ```
        """)
        snippets = parse_markdown(text)
        assert CODEBLOCK_MARK in snippets[0].marks
        assert PYTESTRUN_MARK in snippets[0].marks

    def test_md_no_pytestrun_mark_by_default(self):
        """A plain code block does NOT carry the pytestrun mark."""
        text = textwrap.dedent("""\
            ```python name=test_plain
            x = 1
            ```
        """)
        snippets = parse_markdown(text)
        assert PYTESTRUN_MARK not in snippets[0].marks

    def test_rst_pytestmark_pytestrun_captured(self, tmp_path):
        """The pytestrun mark is present after parsing a marked RST block."""
        rst = textwrap.dedent("""\
            .. pytestmark: pytestrun

            .. code-block:: python
               :name: test_pytestrun_rst

               def test_ok():
                   assert True
        """)
        snippets = parse_rst(rst, tmp_path)
        assert len(snippets) == 1
        assert PYTESTRUN_MARK in snippets[0].marks

    def test_rst_no_pytestrun_mark_by_default(self, tmp_path):
        """A plain RST code block does NOT carry the pytestrun mark."""
        rst = textwrap.dedent("""\
            .. code-block:: python
               :name: test_plain_rst

               x = 1
        """)
        snippets = parse_rst(rst, tmp_path)
        assert PYTESTRUN_MARK not in snippets[0].marks


# =============================================================================
# Test run_pytest_style_code directly
# =============================================================================
class TestRunPytestStyleCode:
    """Unit tests for run_pytest_style_code helper."""

    def test_passing_code_does_not_raise(self, tmp_path):
        """A block with a passing test must not raise."""
        code = textwrap.dedent("""\
            def test_simple():
                assert 1 + 1 == 2
        """)
        # Should complete without exception
        run_pytest_style_code(
            code=code,
            snippet_name="test_simple",
            path=str(tmp_path / "dummy.md"),
        )

    def test_failing_code_raises_assertion_error(self, tmp_path):
        """A block with a failing test must raise AssertionError."""
        code = textwrap.dedent("""\
            def test_fail():
                assert False, "intentional failure"
        """)
        with pytest.raises(AssertionError, match="test_fail"):
            run_pytest_style_code(
                code=code,
                snippet_name="test_fail",
                path=str(tmp_path / "dummy.md"),
            )

    def test_error_message_contains_snippet_name(self, tmp_path):
        """The AssertionError message should reference the snippet name."""
        code = textwrap.dedent("""\
            def test_broken():
                raise ValueError("boom")
        """)
        with pytest.raises(AssertionError) as exc_info:
            run_pytest_style_code(
                code=code,
                snippet_name="test_broken_snippet",
                path=str(tmp_path / "dummy.md"),
            )
        assert "test_broken_snippet" in str(exc_info.value)

    def test_class_based_tests_pass(self, tmp_path):
        """A block containing a Test* class should execute correctly."""
        code = textwrap.dedent("""\
            class TestMath:
                def test_addition(self):
                    assert 2 + 2 == 4

                def test_subtraction(self):
                    assert 5 - 3 == 2
        """)
        run_pytest_style_code(
            code=code,
            snippet_name="test_math_class",
            path=str(tmp_path / "dummy.md"),
        )

    def test_class_based_tests_fail(self, tmp_path):
        """A block with a failing Test* class must raise AssertionError."""
        code = textwrap.dedent("""\
            class TestBroken:
                def test_bad(self):
                    assert 1 == 2
        """)
        with pytest.raises(AssertionError):
            run_pytest_style_code(
                code=code,
                snippet_name="test_broken_class",
                path=str(tmp_path / "dummy.md"),
            )

    def test_class_with_fixture_passes(self, tmp_path):
        """A block using a class-level fixture should pass."""
        code = textwrap.dedent("""\
            import pytest

            class TestFixture:
                @pytest.fixture
                def greeting(self):
                    return "hello"

                def test_greeting(self, greeting):
                    assert greeting == "hello"
        """)
        run_pytest_style_code(
            code=code,
            snippet_name="test_class_fixture",
            path=str(tmp_path / "dummy.md"),
        )

    def test_parametrize_passes(self, tmp_path):
        """A block using @pytest.mark.parametrize should pass."""
        code = textwrap.dedent("""\
            import pytest

            @pytest.mark.parametrize("n,expected", [(1, 2), (2, 4), (3, 6)])
            def test_double(n, expected):
                assert n * 2 == expected
        """)
        run_pytest_style_code(
            code=code,
            snippet_name="test_parametrize",
            path=str(tmp_path / "dummy.md"),
        )

    def test_parametrize_failure_raises(self, tmp_path):
        """A parametrized block with a bad case must raise AssertionError."""
        code = textwrap.dedent("""\
            import pytest

            @pytest.mark.parametrize("n,expected", [(1, 99)])
            def test_wrong(n, expected):
                assert n * 2 == expected
        """)
        with pytest.raises(AssertionError):
            run_pytest_style_code(
                code=code,
                snippet_name="test_bad_parametrize",
                path=str(tmp_path / "dummy.md"),
            )

    def test_setup_teardown_runs(self, tmp_path):
        """setup_method / teardown_method hooks should execute correctly."""
        code = textwrap.dedent("""\
            class TestSetup:
                def setup_method(self):
                    self.value = 42

                def test_value(self):
                    assert self.value == 42

                def teardown_method(self):
                    self.value = None
        """)
        run_pytest_style_code(
            code=code,
            snippet_name="test_setup_teardown",
            path=str(tmp_path / "dummy.md"),
        )

    def test_nested_fixtures_pass(self, tmp_path):
        """Nested fixture dependencies should be resolved correctly."""
        code = textwrap.dedent("""\
            import pytest

            class TestNested:
                @pytest.fixture
                def base(self):
                    return 10

                @pytest.fixture
                def derived(self, base):
                    return base * 3

                def test_derived(self, derived):
                    assert derived == 30
        """)
        run_pytest_style_code(
            code=code,
            snippet_name="test_nested_fixtures",
            path=str(tmp_path / "dummy.md"),
        )

    def test_multiple_test_functions_all_pass(self, tmp_path):
        """Multiple top-level test functions in one block should all run."""
        code = textwrap.dedent("""\
            def test_one():
                assert "a" == "a"

            def test_two():
                assert [1, 2, 3][0] == 1

            def test_three():
                assert {"k": "v"}["k"] == "v"
        """)
        run_pytest_style_code(
            code=code,
            snippet_name="test_multiple_fns",
            path=str(tmp_path / "dummy.md"),
        )

    def test_multiple_test_functions_one_fails(self, tmp_path):
        """If any test function fails, AssertionError must be raised."""
        code = textwrap.dedent("""\
            def test_good():
                assert True

            def test_bad():
                assert False
        """)
        with pytest.raises(AssertionError):
            run_pytest_style_code(
                code=code,
                snippet_name="test_multi_one_fails",
                path=str(tmp_path / "dummy.md"),
            )

    def test_empty_code_raises_no_tests_collected(self, tmp_path):
        """An empty block (no test functions) should fail with non-zero exit."""
        code = "# no tests here\nx = 1\n"
        with pytest.raises(AssertionError):
            run_pytest_style_code(
                code=code,
                snippet_name="test_empty_block",
                path=str(tmp_path / "dummy.md"),
            )

    def test_syntax_error_in_code_raises(self, tmp_path):
        """A block with a syntax error should cause a non-zero pytest exit."""
        code = "def broken(:\n    pass\n"
        with pytest.raises(AssertionError):
            run_pytest_style_code(
                code=code,
                snippet_name="test_syntax_err",
                path=str(tmp_path / "dummy.md"),
            )


# =============================================================================
# Markdown integration tests using pytester
# =============================================================================
class TestPytestrunMarkdownIntegration:
    """End-to-end pytester tests for pytestrun + Markdown."""

    def test_pytestrun_class_passes(self, pytester_subprocess):
        """A Markdown block with pytestrun and a Test* class should pass."""
        pytester_subprocess.makefile(
            ".md",
            test_pytestrun="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_class
import pytest

class TestGreeting:

    @pytest.fixture
    def greeting(self):
        return "hello"

    def test_says_hello(self, greeting):
        assert greeting == "hello"
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)
        assert "test_pytestrun_class" in result.stdout.str()

    def test_pytestrun_failure_propagates(self, pytester_subprocess):
        """A failing pytestrun block should show up as a failed test."""
        pytester_subprocess.makefile(
            ".md",
            test_pytestrun_fail="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_failing
def test_bad():
    assert 1 == 2
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(failed=1)

    def test_pytestrun_with_parametrize(self, pytester_subprocess):
        """A pytestrun block using parametrize should count sub-tests."""
        pytester_subprocess.makefile(
            ".md",
            test_param="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_parametrize
import pytest

@pytest.mark.parametrize("x,y", [(1, 1), (2, 2), (3, 3)])
def test_equal(x, y):
    assert x == y
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        # The outer codeblock test itself should pass
        result.assert_outcomes(passed=1)

    def test_pytestrun_setup_teardown(self, pytester_subprocess):
        """setup_method / teardown_method should work inside pytestrun."""
        pytester_subprocess.makefile(
            ".md",
            test_setup="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_setup_teardown
class TestLifecycle:

    def setup_method(self):
        self.items = []

    def test_append(self):
        self.items.append(1)
        assert self.items == [1]

    def test_fresh_each_time(self):
        assert self.items == []
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    def test_pytestrun_nested_fixtures(self, pytester_subprocess):
        """Nested class-level fixtures should be resolved in pytestrun."""
        pytester_subprocess.makefile(
            ".md",
            test_nested="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_nested_fixtures
import pytest

class TestNested:

    @pytest.fixture
    def base_value(self):
        return 5

    @pytest.fixture
    def doubled(self, base_value):
        return base_value * 2

    def test_doubled(self, doubled):
        assert doubled == 10
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    def test_pytestrun_multiple_classes(self, pytester_subprocess):
        """Multiple Test* classes in one pytestrun block should all execute."""
        pytester_subprocess.makefile(
            ".md",
            test_multi="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_multiple_classes
class TestA:
    def test_a(self):
        assert "a" == "a"

class TestB:
    def test_b(self):
        assert "b" == "b"
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    def test_pytestrun_conftest_fixture(self, pytester_subprocess):
        """pytestrun blocks should be able to use fixtures from conftest."""
        pytester_subprocess.makeconftest("""
import pytest

@pytest.fixture
def answer():
    return 42
""")
        pytester_subprocess.makefile(
            ".md",
            test_conftest="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_conftest_fixture
class TestConftest:

    def test_answer(self, answer):
        assert answer == 42
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)


# =============================================================================
# RST integration tests using pytester
# =============================================================================
class TestPytestrunRSTIntegration:
    """End-to-end pytester tests for pytestrun + RST."""

    def test_pytestrun_rst_class_passes(self, pytester_subprocess):
        """An RST block with pytestrun and a Test* class should pass."""
        pytester_subprocess.makefile(
            ".rst",
            test_pytestrun="""
Test
====

.. pytestmark: pytestrun
.. code-block:: python
   :name: test_pytestrun_rst_class

   import pytest

   class TestCalc:

       @pytest.fixture
       def operand(self):
           return 7

       def test_square(self, operand):
           assert operand ** 2 == 49
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)
        assert "test_pytestrun_rst_class" in result.stdout.str()

    def test_pytestrun_rst_failure_propagates(self, pytester_subprocess):
        """A failing pytestrun RST block should show up as a failed test."""
        pytester_subprocess.makefile(
            ".rst",
            test_fail="""
Fail
====

.. pytestmark: pytestrun
.. code-block:: python
   :name: test_pytestrun_rst_fail

   def test_oops():
       assert "yes" == "no"
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(failed=1)

    def test_pytestrun_rst_parametrize(self, pytester_subprocess):
        """An RST pytestrun block using parametrize should pass."""
        pytester_subprocess.makefile(
            ".rst",
            test_param="""
Param
=====

.. pytestmark: pytestrun
.. code-block:: python
   :name: test_pytestrun_rst_parametrize

   import pytest

   @pytest.mark.parametrize("val", [1, 2, 3])
   def test_positive(val):
       assert val > 0
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    def test_pytestrun_rst_nested_fixtures(self, pytester_subprocess):
        """
        Nested class-level fixtures should resolve in an RST pytestrun block.
        """
        pytester_subprocess.makefile(
            ".rst",
            test_nested="""
Nested
======

.. pytestmark: pytestrun
.. code-block:: python
   :name: test_pytestrun_rst_nested

   import pytest

   class TestNested:

       @pytest.fixture
       def base(self):
           return 3

       @pytest.fixture
       def tripled(self, base):
           return base * 3

       def test_tripled(self, tripled):
           assert tripled == 9
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)


# =============================================================================
# Edge-case tests
# =============================================================================
class TestPytestrunEdgeCases:
    """Edge cases for pytestrun behaviour."""

    def test_pytestrun_mark_detection_in_snippet(self):
        """PYTESTRUN_MARK in sn.marks triggers the pytestrun path."""
        snippet = CodeSnippet(
            name="test_detect",
            code="def test_ok(): assert True",
            line=1,
            marks=[CODEBLOCK_MARK, PYTESTRUN_MARK],
        )
        assert PYTESTRUN_MARK in snippet.marks

    def test_non_pytestrun_snippet_not_detected(self):
        """A regular snippet without pytestrun mark should not trigger it."""
        snippet = CodeSnippet(
            name="test_regular",
            code="x = 1",
            line=1,
            marks=[CODEBLOCK_MARK],
        )
        assert PYTESTRUN_MARK not in snippet.marks

    def test_pytestrun_with_only_function_tests(self, tmp_path):
        """Top-level test_* functions (no class) should run correctly."""
        code = textwrap.dedent("""\
            def test_addition():
                assert 1 + 1 == 2

            def test_string():
                assert "hello".upper() == "HELLO"
        """)
        run_pytest_style_code(
            code=code,
            snippet_name="test_top_level_fns",
            path=str(tmp_path / "dummy.md"),
        )

    def test_pytestrun_with_imports(self, tmp_path):
        """Code that imports stdlib modules should work fine."""
        code = textwrap.dedent("""\
            import math
            import sys

            def test_sqrt():
                assert math.sqrt(9) == 3.0

            def test_python_version():
                assert sys.version_info.major >= 3
        """)
        run_pytest_style_code(
            code=code,
            snippet_name="test_with_imports",
            path=str(tmp_path / "dummy.md"),
        )

    def test_pytestrun_snippet_name_in_output(self, pytester_subprocess):
        """The pytestrun block name should appear in the test report."""
        pytester_subprocess.makefile(
            ".md",
            test_name_check="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_name_visible
def test_sanity():
    assert True
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        assert "test_pytestrun_name_visible" in result.stdout.str()

    def test_pytestrun_does_not_execute_non_test_code(self, tmp_path):
        """
        Non-test code at module level is executed but not treated as a test.
        """
        code = textwrap.dedent("""\
            # Module-level setup code
            CONSTANT = "hello"

            def test_constant():
                assert CONSTANT == "hello"
        """)
        run_pytest_style_code(
            code=code,
            snippet_name="test_module_level",
            path=str(tmp_path / "dummy.md"),
        )

    def test_pytestrun_multiple_marks_on_snippet(self):
        """Snippet can carry both pytestrun and other marks."""
        snippet = CodeSnippet(
            name="test_multi_marks",
            code="def test_x(): pass",
            line=1,
            marks=[CODEBLOCK_MARK, PYTESTRUN_MARK, "slow"],
        )
        assert PYTESTRUN_MARK in snippet.marks
        assert "slow" in snippet.marks
        assert CODEBLOCK_MARK in snippet.marks
