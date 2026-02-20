"""
Tests for the `pytestrun` marker functionality.

When a code block is marked with ``pytestrun``, the plugin writes the block to
a temporary file and executes it via pytest as a subprocess, so that
``Test*`` classes, ``test_*`` functions, fixtures, markers, and
setup/teardown all behave exactly as they would in a normal pytest run.
"""
import textwrap

import pytest

from ..constants import CODEBLOCK_MARK, PYTESTRUN_MARK
from ..md import parse_markdown
from ..pytestrun import run_pytest_style_code
from ..rst import parse_rst

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "TestPytestrunMarkParsing",
    "TestRunPytestStyleCode",
)


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
