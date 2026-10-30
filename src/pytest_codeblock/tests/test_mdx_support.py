"""
Tests for MDX support.

MDX files are collected by default and handled by the Markdown parser.
MDX does not allow HTML comments, so directives can also be written as JSX
comments, for example ``{/* pytestmark: xfail */}``.

Tests cover:
- Collection of ``.mdx`` files
- JSX comment directives
- Integration scenarios
"""
from unittest.mock import MagicMock, patch

from .. import pytest_collect_file
from ..config import Config
from ..constants import CODEBLOCK_MARK
from ..md import MarkdownFile, parse_markdown

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "TestCollectMDXFile",
    "TestJSXDirectives",
    "TestIntegration",
)

MDX_PYPROJECT = """
[tool.pytest-codeblock]
md_user_extensions = [".mdx"]
"""


# ============================================================================
# Test collection of .mdx files
# ============================================================================
class TestCollectMDXFile:
    """Test that .mdx files are collected."""

    def test_mdx_in_default_extensions(self):
        """Test .mdx is one of the default Markdown extensions."""
        assert ".mdx" in Config().all_md_extensions

    # ------------------------------------------------------------------------

    def test_mdx_collected_by_default(self, tmp_path):
        """Test .mdx file returns MarkdownFile with the default config."""
        mdx_file = tmp_path / "doc.mdx"
        mdx_file.write_text("# Doc")

        parent = MagicMock()
        parent.path = tmp_path
        parent.session = MagicMock()
        parent.config = MagicMock()

        with patch("pytest_codeblock.get_config") as mock_get_config:
            mock_get_config.return_value = Config()
            result = pytest_collect_file(parent=parent, file_path=mdx_file)
        assert isinstance(result, MarkdownFile)

    # ------------------------------------------------------------------------

    def test_mdx_not_collected_when_removed(self, tmp_path):
        """Test .mdx file is ignored when removed from md_extensions."""
        mdx_file = tmp_path / "doc.mdx"
        mdx_file.write_text("# Doc")

        parent = MagicMock()
        with patch("pytest_codeblock.get_config") as mock_get_config:
            mock_get_config.return_value = Config(
                md_extensions=(".md", ".markdown")
            )
            result = pytest_collect_file(parent=parent, file_path=mdx_file)
        assert result is None


# ============================================================================
# Test JSX comment directives
# ============================================================================
class TestJSXDirectives:
    """Test directives written as JSX comments (``{/* ... */}``)."""

    def test_pytestmark(self):
        """Test pytestmark in a JSX comment."""
        text = """
{/* pytestmark: xfail */}
```python name=test_example
assert False
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].marks == [CODEBLOCK_MARK, "xfail"]

    # ------------------------------------------------------------------------

    def test_pytestfixture(self):
        """Test pytestfixture in a JSX comment."""
        text = """
{/* pytestfixture: tmp_path */}
```python name=test_example
assert tmp_path.exists()
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].fixtures == ["tmp_path"]

    # ------------------------------------------------------------------------

    def test_continue(self):
        """Test continue in a JSX comment."""
        text = """
```python name=test_setup
x = 1
```

{/* continue: test_setup */}
```python
assert x == 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 2
        assert snippets[1].group == "test_setup"

    # ------------------------------------------------------------------------

    def test_codeblock_name(self):
        """Test codeblock-name in a JSX comment."""
        text = """
{/* codeblock-name: test_named */}
```python
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].name == "test_named"

    # ------------------------------------------------------------------------

    def test_without_spaces(self):
        """Test JSX comment without spaces around the directive."""
        text = """
{/*pytestmark:skip*/}
```python name=test_example
x = 1
```
"""
        snippets = parse_markdown(text)
        assert snippets[0].marks == [CODEBLOCK_MARK, "skip"]

    # ------------------------------------------------------------------------

    def test_mixed_with_html_comments(self):
        """Test HTML and JSX comments can be combined."""
        text = """
<!-- pytestmark: skip -->
{/* pytestmark: slow */}
<!-- pytestfixture: tmp_path -->
{/* pytestfixture: capsys */}
```python name=test_example
x = 1
```
"""
        snippets = parse_markdown(text)
        assert snippets[0].marks == [CODEBLOCK_MARK, "skip", "slow"]
        assert snippets[0].fixtures == ["tmp_path", "capsys"]

    # ------------------------------------------------------------------------

    def test_malformed_directive_ignored(self):
        """Test JSX comment without a value is ignored."""
        text = """
{/* pytestmark: */}
```python name=test_example
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].marks == [CODEBLOCK_MARK]

    # ------------------------------------------------------------------------

    def test_mismatched_delimiters_ignored(self):
        """Test a comment opened as HTML and closed as JSX is ignored."""
        text = """
<!-- pytestmark: xfail */}
```python name=test_example
x = 1
```
"""
        snippets = parse_markdown(text)
        assert snippets[0].marks == [CODEBLOCK_MARK]

    # ------------------------------------------------------------------------

    def test_jsx_content_ignored(self):
        """Test imports, exports and components do not break parsing."""
        text = """
import { Callout } from './callout'

export const meta = { title: 'Doc' }

<Callout type="info">
  Some text.
</Callout>

```python name=test_example
x = 1
```

```javascript name=test_js
console.log(1)
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1
        assert snippets[0].name == "test_example"


# ============================================================================
# Test Integration Scenarios
# ============================================================================
class TestIntegration:
    """Integration tests using pytester."""

    def test_mdx_blocks_are_collected(self, pytester_subprocess):
        """Test Python blocks in .mdx files are collected and run."""
        pytester_subprocess.makefile(".mdx", doc="""
# My Doc

import { Callout } from './callout'

Some <Callout>tag</Callout> here.

```python name=test_mdx_block
x = 2 + 2
assert x == 4
```
""")

        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)
        assert "test_mdx_block" in result.stdout.str()

    # ------------------------------------------------------------------------

    def test_mdx_block_failure_is_detected(self, pytester_subprocess):
        """Test a failing block in an .mdx file fails the run."""
        pytester_subprocess.makefile(".mdx", doc="""
```python name=test_failing_block
assert 1 == 2, "intentional failure"
```
""")

        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(failed=1)
        assert result.ret != 0
        assert "test_failing_block" in result.stdout.str()

    # ------------------------------------------------------------------------

    def test_language_tags(self, pytester_subprocess):
        """Test python3 blocks run and javascript blocks are ignored."""
        pytester_subprocess.makefile(".mdx", doc="""
```python3 name=test_python3_block
assert 1 + 1 == 2
```

```javascript name=test_javascript_block
throw new Error("must not run")
```
""")

        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)
        assert "test_python3_block" in result.stdout.str()
        assert "test_javascript_block" not in result.stdout.str()

    # ------------------------------------------------------------------------

    def test_nameless_codeblocks(self, pytester_subprocess):
        """Test nameless blocks in .mdx files when enabled."""
        pytester_subprocess.makepyprojecttoml("""
[tool.pytest-codeblock]
test_nameless_codeblocks = true
""")
        pytester_subprocess.makefile(".mdx", doc="""
```python
x = 1
assert x == 1
```
""")

        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)
        assert "test_doc_1" in result.stdout.str()

    # ------------------------------------------------------------------------

    def test_md_user_extensions_still_supported(self, pytester_subprocess):
        """Test registering .mdx explicitly does not collect blocks twice."""
        pytester_subprocess.makepyprojecttoml(MDX_PYPROJECT)
        pytester_subprocess.makefile(".mdx", doc="""
```python name=test_mdx_block
x = 1
```
""")

        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    # ------------------------------------------------------------------------

    def test_mdx_not_collected_when_removed(self, pytester_subprocess):
        """Test .mdx files are ignored when removed from md_extensions."""
        pytester_subprocess.makepyprojecttoml("""
[tool.pytest-codeblock]
md_extensions = [".md", ".markdown"]
""")
        pytester_subprocess.makefile(".mdx", doc="""
```python name=test_mdx_block
x = 1
```
""")

        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        # Exit code 5 = no tests collected
        assert result.ret == 5

    # ------------------------------------------------------------------------

    def test_jsx_directives(self, pytester_subprocess):
        """Test markers, fixtures and grouping in JSX comments."""
        # Nameless blocks must be enabled, otherwise the unnamed
        # continuation block is dropped before grouping.
        pytester_subprocess.makepyprojecttoml("""
[tool.pytest-codeblock]
test_nameless_codeblocks = true
""")
        pytester_subprocess.makefile(".mdx", doc="""
{/* pytestmark: xfail */}
```python name=test_xfail_block
assert False
```

{/* pytestfixture: tmp_path */}
```python name=test_fixture_block
file_path = tmp_path / "example.txt"
file_path.write_text("Hello, World!")
assert file_path.read_text() == "Hello, World!"
```

```python name=test_grouped_block
x = 1
```

{/* continue: test_grouped_block */}
```python
assert x == 1
```
""")

        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=3, xfailed=1)
        assert "test_fixture_block" in result.stdout.str()
        assert "test_grouped_block" in result.stdout.str()
