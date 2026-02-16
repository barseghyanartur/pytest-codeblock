from pathlib import Path

from .config import get_config
from .constants import CODEBLOCK_MARK
from .md import MarkdownFile
from .rst import RSTFile

__title__ = "pytest-codeblock"
__version__ = "0.5.1"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "pytest_collect_file",
    "pytest_configure",
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


def pytest_configure(config):
    """Register the codeblock marker if not already registered."""
    # Get existing markers
    existing_markers = config.getini("markers")
    marker_names = [m.split(":")[0].strip() for m in existing_markers]

    # Only register if not already present
    if CODEBLOCK_MARK not in marker_names:
        config.addinivalue_line(
            "markers",
            f"{CODEBLOCK_MARK}: pytest-codeblock markers (auto-registered)",
        )
