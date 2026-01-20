from dataclasses import dataclass, field
from typing import Optional

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
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
    fixtures: list[str] = field(default_factory=list)
    # Collected pytest fixtures (e.g. ['tmp_path']), parsed from doc comments


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
            seen_sn.code += "\n" + sn.code
            seen_sn.marks.extend(sn.marks)
            seen_sn.fixtures.extend(sn.fixtures)
        else:
            sn.marks = list(sn.marks)  # copy
            sn.fixtures = list(sn.fixtures)  # copy
            seen[key] = sn
            combined.append(sn)

    return combined
