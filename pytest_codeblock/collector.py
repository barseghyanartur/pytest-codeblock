from dataclasses import dataclass, field
from typing import Optional

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "CodeSnippet",
    "group_snippets",
)


@dataclass
class CodeSnippet:
    """Data container for an extracted code snippet."""
    code: str  # The code content
    line: int  # Starting line number in the source
    name: Optional[str] = None  # Identifier for grouping (None if anonymous)
    marks: list[str] = field(default_factory=list)
    # Collected pytest marks (e.g. ['django_db']), parsed from doc comments
    is_literalinclude: bool = False  # Distinguish literalinclude snippets
    file_path: Optional[str] = None  # Literalinclude file paths

    # Highlight: Added method to handle literalinclude content
    def get_content(self) -> str:
        """Get the code content, reading from file if it's a literalinclude."""
        if self.is_literalinclude and self.file_path:
            try:
                with open(self.file_path) as f:
                    return f.read()
            except Exception as e:
                raise RuntimeError(
                    f"Failed to read literalinclude file {self.file_path}: {e}"
                ) from e
        return self.code


def group_snippets(snippets: list[CodeSnippet]) -> list[CodeSnippet]:
    """
    Merge snippets with the same name into one CodeSnippet,
    concatenating their code and accumulating marks.
    Unnamed snippets get unique auto-names.
    """
    combined: list[CodeSnippet] = []
    seen: dict[str, CodeSnippet] = {}
    anon_count = 0

    for sn in snippets:
        key = sn.name
        if not key:
            anon_count += 1
            key = f"codeblock{anon_count}"

        if key in seen:
            seen_sn = seen[key]
            if not sn.is_literalinclude:
                seen_sn.code += "\n" + sn.code
            seen_sn.marks.extend(sn.marks)
        else:
            sn.marks = list(sn.marks)  # copy
            seen[key] = sn
            combined.append(sn)

    return combined
