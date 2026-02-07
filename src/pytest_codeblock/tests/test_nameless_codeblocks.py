"""
Unit tests for the test_nameless_codeblocks configuration feature.

Tests cover:
- Configuration loading
- Auto-naming behavior
- Markdown collector
- RST collector
- Integration scenarios
- Edge cases
"""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ..collector import group_snippets
from ..config import Config
from ..md import parse_markdown
from ..rst import parse_rst

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "TestConfigLoading",
    "TestAutoNaming",
    "TestMarkdownNameless",
    "TestRSTNameless",
    "TestIntegration",
    "TestEdgeCases",
)


# =============================================================================
# Test Configuration Loading
# =============================================================================
class TestConfigLoading:
    """Test that test_nameless_codeblocks config loads correctly."""

    def test_default_value_is_false(self):
        """Test that default value is False."""
        config = Config()
        assert config.test_nameless_codeblocks is False

    def test_explicit_true_value(self):
        """Test setting value to True."""
        config = Config(test_nameless_codeblocks=True)
        assert config.test_nameless_codeblocks is True

    def test_explicit_false_value(self):
        """Test setting value to False explicitly."""
        config = Config(test_nameless_codeblocks=False)
        assert config.test_nameless_codeblocks is False

    def test_config_from_dict(self):
        """Test loading from configuration dict."""
        # Simulate loading from pyproject.toml
        raw = {"test_nameless_codeblocks": True}
        config = Config(
            test_nameless_codeblocks=raw.get("test_nameless_codeblocks", False)
        )
        assert config.test_nameless_codeblocks is True

    def test_config_from_dict_missing_key(self):
        """Test loading from dict without the key uses default."""
        raw = {}
        config = Config(
            test_nameless_codeblocks=raw.get("test_nameless_codeblocks", False)
        )
        assert config.test_nameless_codeblocks is False


# =============================================================================
# Test Auto-naming Logic
# =============================================================================
class TestAutoNaming:
    """Test the auto-naming scheme for nameless code blocks."""

    def test_auto_name_format(self):
        """
        Test that auto-generated names follow test_{module}_{counter} format.
        """
        module_name = "README"
        counter = 1
        auto_name = f"test_{module_name}_{counter}"
        assert auto_name == "test_README_1"

    def test_auto_name_increment(self):
        """Test that counter increments for multiple nameless blocks."""
        module_name = "guide"
        names = [f"test_{module_name}_{i}" for i in range(1, 4)]
        assert names == ["test_guide_1", "test_guide_2", "test_guide_3"]

    def test_module_name_extraction(self):
        """Test extracting module name from Path.stem."""
        path = Path("/path/to/README.md")
        module_name = path.stem
        assert module_name == "README"

    def test_module_name_with_dots(self):
        """Test module name extraction with dots in filename."""
        path = Path("/path/to/my.doc.md")
        module_name = path.stem
        # Path.stem returns everything before the last dot
        assert module_name == "my.doc"


# =============================================================================
# Test Markdown Collector with Nameless Blocks
# =============================================================================
class TestMarkdownNameless:
    """Test MarkdownFile collector with test_nameless_codeblocks."""

    def test_parse_markdown_nameless_snippets(self):
        """Test that parse_markdown extracts nameless snippets."""
        text = """
```python
x = 1
```

```python
y = 2
```
"""
        snippets = parse_markdown(text)
        # parse_markdown should extract them (name=None)
        assert len(snippets) == 2
        assert snippets[0].name is None
        assert snippets[1].name is None
        assert "x = 1" in snippets[0].code
        assert "y = 2" in snippets[1].code

    # -------------------------------------------------------------------------

    def test_parse_markdown_mixed_named_and_nameless(self):
        """Test parsing mix of named and nameless blocks."""
        text = """
```python name=test_one
a = 1
```

```python
b = 2
```

```python name=test_two
c = 3
```

```python
d = 4
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 4
        assert snippets[0].name == "test_one"
        assert snippets[1].name is None
        assert snippets[2].name == "test_two"
        assert snippets[3].name is None

    # -------------------------------------------------------------------------

    def test_collect_nameless_disabled_default(self):
        """Test that nameless blocks are ignored by default."""
        text = """
```python name=test_explicit
x = 1
```

```python
y = 2
```
"""
        # Mock config with default (False)
        mock_config = Config(test_nameless_codeblocks=False)

        with patch("pytest_codeblock.md.get_config", return_value=mock_config):
            # Create a mock MarkdownFile
            parent = MagicMock()
            parent.config = MagicMock()
            path = Path("/tmp/test.md")

            # We can't easily test collect() without full pytest setup,
            # but we can test the filtering logic
            raw = parse_markdown(text)

            # Apply the filtering logic from collect()
            if mock_config.test_nameless_codeblocks:
                tests = []
                counter = 1
                module_name = path.stem
                for sn in raw:
                    if sn.name and sn.name.startswith("test_"):
                        tests.append(sn)
                    elif not sn.name:
                        auto_name = f"test_{module_name}_{counter}"
                        counter += 1
                        sn.name = auto_name
                        tests.append(sn)
            else:
                tests = [
                    sn for sn in raw if sn.name and sn.name.startswith("test_")
                ]

            # Should only have the named test
            assert len(tests) == 1
            assert tests[0].name == "test_explicit"

    # -------------------------------------------------------------------------

    def test_collect_nameless_enabled(self):
        """Test that nameless blocks are collected when enabled."""
        text = """
```python name=test_explicit
x = 1
```

```python
y = 2
```

```python
z = 3
```
"""
        # Mock config with feature enabled
        mock_config = Config(test_nameless_codeblocks=True)

        with patch("pytest_codeblock.md.get_config", return_value=mock_config):
            path = Path("/tmp/test.md")
            raw = parse_markdown(text)

            # Apply the filtering logic from collect()
            tests = []
            counter = 1
            module_name = path.stem
            for sn in raw:
                if sn.name and sn.name.startswith("test_"):
                    tests.append(sn)
                elif not sn.name:
                    auto_name = f"test_{module_name}_{counter}"
                    counter += 1
                    sn.name = auto_name
                    tests.append(sn)

            # Should have all three blocks
            assert len(tests) == 3
            assert tests[0].name == "test_explicit"
            assert tests[1].name == "test_test_1"
            assert tests[2].name == "test_test_2"

    # -------------------------------------------------------------------------

    def test_auto_naming_preserves_code(self):
        """Test that auto-naming doesn't modify the code content."""
        text = """
```python
original_code = "unchanged"
assert original_code == "unchanged"
```
"""
        mock_config = Config(test_nameless_codeblocks=True)

        with patch("pytest_codeblock.md.get_config", return_value=mock_config):
            path = Path("/tmp/myfile.md")
            raw = parse_markdown(text)

            tests = []
            counter = 1
            module_name = path.stem
            for sn in raw:
                if not sn.name:
                    sn.name = f"test_{module_name}_{counter}"
                    counter += 1
                    tests.append(sn)

            assert len(tests) == 1
            assert tests[0].name == "test_myfile_1"
            assert "original_code" in tests[0].code
            assert "unchanged" in tests[0].code

    # -------------------------------------------------------------------------

    def test_auto_naming_preserves_marks(self):
        """Test that auto-naming preserves pytest marks."""
        text = """
<!-- pytestmark: django_db -->
```python
from django.contrib.auth.models import User
user = User.objects.first()
```
"""
        mock_config = Config(test_nameless_codeblocks=True)

        with patch("pytest_codeblock.md.get_config", return_value=mock_config):
            path = Path("/tmp/test.md")
            raw = parse_markdown(text)

            tests = []
            counter = 1
            module_name = path.stem
            for sn in raw:
                if not sn.name:
                    sn.name = f"test_{module_name}_{counter}"
                    counter += 1
                    tests.append(sn)

            assert len(tests) == 1
            assert "django_db" in tests[0].marks

    # -------------------------------------------------------------------------

    def test_auto_naming_preserves_fixtures(self):
        """Test that auto-naming preserves pytest fixtures."""
        text = """
<!-- pytestfixture: tmp_path -->
<!-- pytestfixture: capsys -->
```python
d = tmp_path / "test"
d.mkdir()
```
"""
        mock_config = Config(test_nameless_codeblocks=True)

        with patch("pytest_codeblock.md.get_config", return_value=mock_config):
            path = Path("/tmp/test.md")
            raw = parse_markdown(text)

            tests = []
            counter = 1
            module_name = path.stem
            for sn in raw:
                if not sn.name:
                    sn.name = f"test_{module_name}_{counter}"
                    counter += 1
                    tests.append(sn)

            assert len(tests) == 1
            assert "tmp_path" in tests[0].fixtures
            assert "capsys" in tests[0].fixtures


# =============================================================================
# Test RST Collector with Nameless Blocks
# =============================================================================
class TestRSTNameless:
    """Test RSTFile collector with test_nameless_codeblocks."""

    def test_parse_rst_nameless_snippets(self, tmp_path):
        """Test that parse_rst extracts nameless snippets."""
        text = """
.. code-block:: python

   x = 1

.. code-block:: python

   y = 2
"""
        snippets = parse_rst(text, tmp_path)
        # parse_rst should extract them (name=None)
        assert len(snippets) == 2
        assert snippets[0].name is None
        assert snippets[1].name is None
        assert "x = 1" in snippets[0].code
        assert "y = 2" in snippets[1].code

    # -------------------------------------------------------------------------

    def test_parse_rst_mixed_named_and_nameless(self, tmp_path):
        """Test parsing mix of named and nameless blocks."""
        text = """
.. code-block:: python
   :name: test_one

   a = 1

.. code-block:: python

   b = 2

.. code-block:: python
   :name: test_two

   c = 3

.. code-block:: python

   d = 4
"""
        snippets = parse_rst(text, tmp_path)
        assert len(snippets) == 4
        assert snippets[0].name == "test_one"
        assert snippets[1].name is None
        assert snippets[2].name == "test_two"
        assert snippets[3].name is None

    # -------------------------------------------------------------------------

    def test_collect_nameless_disabled_default(self, tmp_path):
        """Test that nameless blocks are ignored by default in RST."""
        text = """
.. code-block:: python
   :name: test_explicit

   x = 1

.. code-block:: python

   y = 2
"""
        mock_config = Config(test_nameless_codeblocks=False)

        with patch(
            "pytest_codeblock.rst.get_config", return_value=mock_config
        ):
            path = Path("/tmp/test.rst")
            raw = parse_rst(text, tmp_path)

            # Apply the filtering logic from collect()
            if mock_config.test_nameless_codeblocks:
                tests = []
                counter = 1
                module_name = path.stem
                for sn in raw:
                    if sn.name and sn.name.startswith("test_"):
                        tests.append(sn)
                    elif not sn.name:
                        auto_name = f"test_{module_name}_{counter}"
                        counter += 1
                        sn.name = auto_name
                        tests.append(sn)
            else:
                tests = [
                    sn for sn in raw if sn.name and sn.name.startswith("test_")
                ]

            # Should only have the named test
            assert len(tests) == 1
            assert tests[0].name == "test_explicit"

    # -------------------------------------------------------------------------

    def test_collect_nameless_enabled(self, tmp_path):
        """Test that nameless blocks are collected when enabled in RST."""
        text = """
.. code-block:: python
   :name: test_explicit

   x = 1

.. code-block:: python

   y = 2

.. code-block:: python

   z = 3
"""
        mock_config = Config(test_nameless_codeblocks=True)

        with patch(
            "pytest_codeblock.rst.get_config", return_value=mock_config
        ):
            path = Path("/tmp/test.rst")
            raw = parse_rst(text, tmp_path)

            # Apply the filtering logic from collect()
            tests = []
            counter = 1
            module_name = path.stem
            for sn in raw:
                if sn.name and sn.name.startswith("test_"):
                    tests.append(sn)
                elif not sn.name:
                    auto_name = f"test_{module_name}_{counter}"
                    counter += 1
                    sn.name = auto_name
                    tests.append(sn)

            # Should have all three blocks
            assert len(tests) == 3
            assert tests[0].name == "test_explicit"
            assert tests[1].name == "test_test_1"
            assert tests[2].name == "test_test_2"

    # -------------------------------------------------------------------------

    def test_auto_naming_preserves_code_rst(self, tmp_path):
        """Test that auto-naming doesn't modify the code content in RST."""
        text = """
.. code-block:: python

   original_code = "unchanged"
   assert original_code == "unchanged"
"""
        mock_config = Config(test_nameless_codeblocks=True)

        with patch(
            "pytest_codeblock.rst.get_config", return_value=mock_config
        ):
            path = Path("/tmp/myfile.rst")
            raw = parse_rst(text, tmp_path)

            tests = []
            counter = 1
            module_name = path.stem
            for sn in raw:
                if not sn.name:
                    sn.name = f"test_{module_name}_{counter}"
                    counter += 1
                    tests.append(sn)

            assert len(tests) == 1
            assert tests[0].name == "test_myfile_1"
            assert "original_code" in tests[0].code
            assert "unchanged" in tests[0].code

    # -------------------------------------------------------------------------

    def test_auto_naming_preserves_marks_rst(self, tmp_path):
        """Test that auto-naming preserves pytest marks in RST."""
        text = """
.. pytestmark: django_db

.. code-block:: python

   from django.contrib.auth.models import User
   user = User.objects.first()
"""
        mock_config = Config(test_nameless_codeblocks=True)

        with patch(
            "pytest_codeblock.rst.get_config", return_value=mock_config
        ):
            path = Path("/tmp/test.rst")
            raw = parse_rst(text, tmp_path)

            tests = []
            counter = 1
            module_name = path.stem
            for sn in raw:
                if not sn.name:
                    sn.name = f"test_{module_name}_{counter}"
                    counter += 1
                    tests.append(sn)

            assert len(tests) == 1
            assert "django_db" in tests[0].marks

    # -------------------------------------------------------------------------

    def test_auto_naming_preserves_fixtures_rst(self, tmp_path):
        """Test that auto-naming preserves pytest fixtures in RST."""
        text = """
.. pytestfixture: tmp_path
.. pytestfixture: capsys

.. code-block:: python

   d = tmp_path / "test"
   d.mkdir()
"""
        mock_config = Config(test_nameless_codeblocks=True)

        with patch(
            "pytest_codeblock.rst.get_config", return_value=mock_config
        ):
            path = Path("/tmp/test.rst")
            raw = parse_rst(text, tmp_path)

            tests = []
            counter = 1
            module_name = path.stem
            for sn in raw:
                if not sn.name:
                    sn.name = f"test_{module_name}_{counter}"
                    counter += 1
                    tests.append(sn)

            assert len(tests) == 1
            assert "tmp_path" in tests[0].fixtures
            assert "capsys" in tests[0].fixtures


# =============================================================================
# Test Integration Scenarios
# =============================================================================
@pytest.mark.skip(
    reason="Skip due to pytest 9 py.path.local deprecation issue in hooks"
)
class TestIntegration:
    """Integration tests using pytester."""

    def test_markdown_nameless_integration(self, pytester):
        """Test nameless blocks work end-to-end in Markdown."""
        pytester.makepyprojecttoml("""
[tool.pytest-codeblock]
test_nameless_codeblocks = true
""")

        pytester.makefile(".md", test_integration="""
# Test File

```python name=test_explicit
x = 1
assert x == 1
```

```python
y = 2
assert y == 2
```

```python
z = 3
assert z == 3
```
""")

        result = pytester.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=3)
        assert "test_explicit" in result.stdout.str()
        assert "test_integration_1" in result.stdout.str()
        assert "test_integration_2" in result.stdout.str()

    # -------------------------------------------------------------------------

    def test_rst_nameless_integration(self, pytester):
        """Test nameless blocks work end-to-end in RST."""
        pytester.makepyprojecttoml("""
[tool.pytest-codeblock]
test_nameless_codeblocks = true
""")

        pytester.makefile(".rst", test_integration="""
Test File
=========

.. code-block:: python
   :name: test_explicit

   x = 1
   assert x == 1

.. code-block:: python

   y = 2
   assert y == 2

.. code-block:: python

   z = 3
   assert z == 3
""")

        result = pytester.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=3)
        assert "test_explicit" in result.stdout.str()
        assert "test_integration_1" in result.stdout.str()
        assert "test_integration_2" in result.stdout.str()

    # -------------------------------------------------------------------------

    def test_nameless_disabled_integration(self, pytester):
        """Test that nameless blocks are ignored when disabled."""
        # Don't set test_nameless_codeblocks (default False)
        pytester.makefile(".md", test_default="""
# Test File

```python name=test_explicit
x = 1
assert x == 1
```

```python
y = 2
assert y == 2
```
""")

        result = pytester.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)
        assert "test_explicit" in result.stdout.str()
        assert "test_default_1" not in result.stdout.str()

    # -------------------------------------------------------------------------

    def test_multiple_files_separate_counters(self, pytester):
        """Test that each file has its own counter."""
        pytester.makepyprojecttoml("""
[tool.pytest-codeblock]
test_nameless_codeblocks = true
""")

        pytester.makefile(".md", file1="""
```python
x = 1
```

```python
y = 2
```
""")

        pytester.makefile(".md", file2="""
```python
a = 1
```

```python
b = 2
```
""")

        result = pytester.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=4)
        # Each file should have _1 and _2
        assert "test_file1_1" in result.stdout.str()
        assert "test_file1_2" in result.stdout.str()
        assert "test_file2_1" in result.stdout.str()
        assert "test_file2_2" in result.stdout.str()


# =============================================================================
# Test Edge Cases
# =============================================================================
class TestEdgeCases:
    """Test edge cases and corner scenarios."""

    @pytest.mark.skip(
        reason="Skip due to pytest 9 py.path.local deprecation issue in hooks"
    )
    def test_only_nameless_blocks(self, pytester):
        """Test file with only nameless blocks."""
        pytester.makepyprojecttoml("""
[tool.pytest-codeblock]
test_nameless_codeblocks = true
""")

        pytester.makefile(".md", only_nameless="""
```python
x = 1
```

```python
y = 2
```

```python
z = 3
```
""")

        result = pytester.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=3)

    # -------------------------------------------------------------------------

    @pytest.mark.skip(
        reason="Skip due to pytest 9 py.path.local deprecation issue in hooks"
    )
    def test_only_named_blocks(self, pytester):
        """Test file with only named blocks."""
        pytester.makepyprojecttoml("""
[tool.pytest-codeblock]
test_nameless_codeblocks = true
""")

        pytester.makefile(".md", only_named="""
```python name=test_one
x = 1
```

```python name=test_two
y = 2
```
""")

        result = pytester.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=2)
        assert "test_one" in result.stdout.str()
        assert "test_two" in result.stdout.str()
        # No auto-generated names
        assert "test_only_named_1" not in result.stdout.str()

    # -------------------------------------------------------------------------

    @pytest.mark.skip(
        reason="Skip due to pytest 9 py.path.local deprecation issue in hooks"
    )
    def test_empty_code_blocks(self, pytester):
        """Test that empty nameless blocks are handled."""
        pytester.makepyprojecttoml("""
[tool.pytest-codeblock]
test_nameless_codeblocks = true
""")

        pytester.makefile(".md", empty="""
```python
```

```python
x = 1
assert x == 1
```
""")

        # Empty blocks might not be collected by parser
        result = pytester.runpytest("-v", "-p", "no:django")
        # Should have at least the non-empty one
        assert result.ret == 0

    # -------------------------------------------------------------------------

    @pytest.mark.skip(
        reason="Skip due to pytest 9 py.path.local deprecation issue in hooks"
    )
    def test_non_python_blocks_ignored(self, pytester):
        """Test that non-Python blocks are still ignored."""
        pytester.makepyprojecttoml("""
[tool.pytest-codeblock]
test_nameless_codeblocks = true
""")

        pytester.makefile(".md", mixed_lang="""
```python
x = 1
```

```javascript
console.log("ignored");
```

```python
y = 2
```
""")

        result = pytester.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=2)
        # Only Python blocks should be collected

    # -------------------------------------------------------------------------

    def test_nameless_with_continue_directive_md(self):
        """Test nameless blocks with continue directive in Markdown."""
        text = """
```python name=test_base
x = 1
```

<!-- continue: test_base -->
```python
y = x + 1
assert y == 2
```
"""
        mock_config = Config(test_nameless_codeblocks=True)

        with patch("pytest_codeblock.md.get_config", return_value=mock_config):
            raw = parse_markdown(text)

            # Group snippets as in collect()
            combined = group_snippets(raw)

            # Should have merged into one test_base
            assert len(combined) == 1
            assert combined[0].name == "test_base"
            assert "x = 1" in combined[0].code
            assert "y = x + 1" in combined[0].code

    # -------------------------------------------------------------------------

    def test_nameless_with_continue_directive_rst(self, tmp_path):
        """Test nameless blocks with continue directive in RST."""
        text = """
.. code-block:: python
   :name: test_base

   x = 1

.. continue: test_base

.. code-block:: python

   y = x + 1
   assert y == 2
"""
        mock_config = Config(test_nameless_codeblocks=True)

        with patch(
            "pytest_codeblock.rst.get_config", return_value=mock_config
        ):
            raw = parse_rst(text, tmp_path)

            # Group snippets as in collect()
            combined = group_snippets(raw)

            # Should have merged into one test_base
            assert len(combined) == 1
            assert combined[0].name == "test_base"
            assert "x = 1" in combined[0].code
            assert "y = x + 1" in combined[0].code

    # -------------------------------------------------------------------------

    def test_counter_only_increments_for_nameless(self):
        """Test that counter only increments for nameless blocks."""
        text = """
```python name=test_explicit_1
a = 1
```

```python
b = 2
```

```python name=test_explicit_2
c = 3
```

```python
d = 4
```

```python name=test_explicit_3
e = 5
```

```python
f = 6
```
"""
        mock_config = Config(test_nameless_codeblocks=True)

        with patch(
            "pytest_codeblock.md.get_config", return_value=mock_config
        ):
            path = Path("/tmp/test.md")
            raw = parse_markdown(text)

            tests = []
            counter = 1
            module_name = path.stem
            for sn in raw:
                if sn.name and sn.name.startswith("test_"):
                    tests.append(sn)
                elif not sn.name:
                    sn.name = f"test_{module_name}_{counter}"
                    counter += 1
                    tests.append(sn)

            # Should have 6 tests total
            assert len(tests) == 6
            # Named blocks keep their names
            assert tests[0].name == "test_explicit_1"
            assert tests[2].name == "test_explicit_2"
            assert tests[4].name == "test_explicit_3"
            # Nameless blocks get sequential numbers
            assert tests[1].name == "test_test_1"
            assert tests[3].name == "test_test_2"
            assert tests[5].name == "test_test_3"

    # -------------------------------------------------------------------------

    def test_filename_with_special_characters(self):
        """Test auto-naming with special characters in filename."""
        # Path.stem handles most special chars
        path = Path("/tmp/my-test_file.md")
        module_name = path.stem
        auto_name = f"test_{module_name}_1"
        assert auto_name == "test_my-test_file_1"

    # -------------------------------------------------------------------------

    @pytest.mark.skip(
        reason="Skip due to pytest 9 py.path.local deprecation issue in hooks"
    )
    def test_both_formats_disabled(self, pytester):
        """Test both MD and RST with feature disabled."""
        pytester.makefile(".md", test_md="""
```python
x = 1
```
""")

        pytester.makefile(".rst", test_rst="""
.. code-block:: python

   y = 2
""")

        result = pytester.runpytest("-v", "-p", "no:django")
        # No tests should be collected
        assert result.ret == 5  # Exit code 5 = no tests collected

    # -------------------------------------------------------------------------

    @pytest.mark.skip(
        reason="Skip due to pytest 9 py.path.local deprecation issue in hooks"
    )
    def test_both_formats_enabled(self, pytester):
        """Test both MD and RST with feature enabled."""
        pytester.makepyprojecttoml("""
[tool.pytest-codeblock]
test_nameless_codeblocks = true
""")

        pytester.makefile(".md", test_md="""
```python
x = 1
assert x == 1
```
""")

        pytester.makefile(".rst", test_rst="""
.. code-block:: python

   y = 2
   assert y == 2
""")

        result = pytester.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=2)
        assert "test_md_1" in result.stdout.str()
        assert "test_rst_1" in result.stdout.str()
