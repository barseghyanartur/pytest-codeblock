from pathlib import Path

from .config import get_config
from .md import MarkdownFile
from .rst import RSTFile

__title__ = "pytest-codeblock"
__version__ = "0.4"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "pytest_collect_file",
)


def pytest_collect_file(parent, path):
    """Collect .md and .rst files for codeblock tests."""
    config = get_config()
    # Determine file extension (works for py.path or pathlib.Path)
    file_name = str(path).lower()
    if any(file_name.endswith(ext) for ext in config.all_md_extensions):
        # Use the MarkdownFile collector for Markdown files
        return MarkdownFile.from_parent(parent=parent, path=Path(path))
    if any(file_name.endswith(ext) for ext in config.all_rst_extensions):
        # Use the RSTFile collector for reStructuredText files
        return RSTFile.from_parent(parent=parent, path=Path(path))
    return None
