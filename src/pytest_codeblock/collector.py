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
    group: Optional[str] = None
    # Set by ``continue:`` directives; names the group this snippet belongs to


def group_snippets(snippets: list[CodeSnippet]) -> list[CodeSnippet]:
    """
    Combine snippets that share a group key, using one of two modes:

    - Merge mode (default): snippets sharing the same name (no ``group``
      set, or nameless/same-name continuations) are concatenated into a single
      test, accumulating marks and fixtures. This is the default behaviour.
    - Incremental mode: when every continuation snippet (``group`` set) in
      a group also carries its own distinct name, emit one test per snippet.
      Each test's code is the cumulative concatenation of all preceding
      snippets plus itself, so each step is exercised in isolation.

    Unnamed snippets receive unique auto-keys so they are never merged.
    """
    # Pass 1: bucket each snippet by its group key, preserving insertion order.
    buckets: dict[str, list[CodeSnippet]] = {}
    order: list[str] = []
    anon_count = 0

    for sn in snippets:
        if sn.group:
            key = sn.group
        elif sn.name:
            key = sn.name
        else:
            anon_count += 1
            key = f"codeblock{anon_count}"

        if key not in buckets:
            buckets[key] = []
            order.append(key)
        buckets[key].append(sn)

    # Pass 2: emit merged or incremental snippets per bucket.
    combined: list[CodeSnippet] = []

    for key in order:
        members = buckets[key]
        continuations = [sn for sn in members if sn.group]
        # Incremental only when every continuation has a distinct own name.
        incremental = continuations and all(
            sn.name and sn.name != key for sn in continuations
        )

        if incremental:
            acc_code = ""
            acc_marks: list[str] = []
            acc_fixtures: list[str] = []
            for sn in members:
                acc_code = acc_code + "\n" + sn.code if acc_code else sn.code
                acc_marks.extend(sn.marks)
                acc_fixtures.extend(sn.fixtures)
                combined.append(CodeSnippet(
                    name=sn.name,
                    code=acc_code,
                    line=sn.line,
                    marks=list(acc_marks),
                    fixtures=list(acc_fixtures),
                ))
        else:
            # Merge mode (default behaviour).
            first = members[0]
            merged_marks = list(first.marks)
            merged_fixtures = list(first.fixtures)
            merged_code = first.code
            for sn in members[1:]:
                merged_code += "\n" + sn.code
                merged_marks.extend(sn.marks)
                merged_fixtures.extend(sn.fixtures)
            combined.append(CodeSnippet(
                name=first.name,
                code=merged_code,
                line=first.line,
                marks=merged_marks,
                fixtures=merged_fixtures,
            ))

    return combined
