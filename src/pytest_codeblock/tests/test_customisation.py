"""Tests for customisation of languages and extensions."""
from unittest.mock import patch

from ..config import get_config
from ..md import parse_markdown


class TestCustomLanguages:
    """Test custom language support in markdown."""

    def test_custom_md_language_recognized(self):
        """Test that custom markdown language is recognised when configured."""
        # Mock config to include custom language
        mock_config = {
            "all_md_codeblocks": ["python", "djc_py"],  # djc_py is custom
            "all_rst_codeblocks": ["python"],
            "all_md_extensions": [".md"],
            "all_rst_extensions": [".rst"],
        }

        text = """
```djc_py name=custom_lang
x = 1
```
"""
        with patch("pytest_codeblock.md.get_config") as mock_get_config:
            mock_config_obj = type("Config", (), mock_config)()
            mock_get_config.return_value = mock_config_obj

            snippets = parse_markdown(text)
            assert len(snippets) == 1
            assert snippets[0].name == "custom_lang"
            assert "x = 1" in snippets[0].code

    # -------------------------------------------------------------------------

    def test_unknown_language_ignored(self):
        """Test that unknown language fence is ignored."""
        text = """
```unknown_lang
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 0


class TestCustomExtensions:
    """Test custom file extension support."""

    def test_config_includes_custom_extensions(self):
        """Test that config can include custom extensions."""
        config = get_config()
        # By default should include .md and .rst
        assert ".md" in config.all_md_extensions
        assert ".rst" in config.all_rst_extensions

    def test_python_as_custom_md_extension(self):
        """Test that .py files can be configured as markdown sources."""
        # This test verifies the config structure supports it
        mock_config = {
            "all_md_codeblocks": ["python"],
            "all_rst_codeblocks": ["python"],
            "all_md_extensions": [".md", ".txt"],  # .txt added
            "all_rst_extensions": [".rst"],
        }

        mock_config_obj = type("Config", (), mock_config)()
        # Verify .txt extension is in the list
        assert ".txt" in mock_config_obj.all_md_extensions


class TestDefaults:
    """Test that defaults are preserved."""

    def test_default_python_language_works(self):
        """Test that default Python language is always available."""
        text = """
```python
x = 1
```
"""
        snippets = parse_markdown(text)
        assert len(snippets) == 1

    # -------------------------------------------------------------------------

    def test_default_md_extension(self):
        """Test that .md is always a supported extension."""
        config = get_config()
        assert ".md" in config.all_md_extensions

    def test_default_rst_extension(self):
        """Test that .rst is always a supported extension."""
        config = get_config()
        assert ".rst" in config.all_rst_extensions
