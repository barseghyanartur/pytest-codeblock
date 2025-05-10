from .md import MarkdownFile
from .rst import RSTFile

__title__ = "pytest-codeblock"
__version__ = "0.1.8"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "pytest_collect_file",
)


def pytest_collect_file(parent, path):
    """Collect .md and .rst files for codeblock tests."""
    # Determine file extension (works for py.path or pathlib.Path)
    file_name = str(path).lower()
    if file_name.endswith((".md", ".markdown")):
        # Use the MarkdownFile collector for Markdown files
        return MarkdownFile.from_parent(parent=parent, fspath=path)
    if file_name.endswith(".rst"):
        # Use the RSTFile collector for reStructuredText files
        return RSTFile.from_parent(parent=parent, fspath=path)
    return None
