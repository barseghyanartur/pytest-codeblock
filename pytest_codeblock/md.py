import re
from typing import Optional

import pytest

from .collector import CodeSnippet, group_snippets
from .constants import CODEBLOCK_MARK, DJANGO_DB_MARKS, TEST_PREFIX

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "MarkdownFile",
    "parse_markdown",
)


def parse_markdown(text: str) -> list[CodeSnippet]:
    """
    Parse Markdown text and extract Python code snippets as CodeSnippet
    objects.

    Supports:
      - <!-- pytestmark: <mark> --> comments immediately before a code fence
      - <!-- codeblock-name: <name> --> comments for naming
      - Fenced code blocks with ```python (and optional name=<name> in the
        info string)

    Captures each snippet’s name, code, starting line, and any pytest marks.
    """
    snippets: list[CodeSnippet] = []
    lines = text.splitlines()
    pending_name: Optional[str] = None
    pending_marks: list[str] = [CODEBLOCK_MARK]
    in_block = False
    fence = ""
    block_indent = 0
    code_buffer: list[str] = []
    snippet_name: Optional[str] = None
    start_line = 0

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not in_block:
            # Check for pytest mark comment
            if stripped.startswith("<!--") and "pytestmark:" in stripped:
                m = re.match(r"<!--\s*pytestmark:\s*(\w+)\s*-->", stripped)
                if m:
                    pending_marks.append(m.group(1))
                continue

            # Check for name comment
            if stripped.startswith("<!--") and "codeblock-name:" in stripped:
                m = re.match(
                    r"<!--\s*codeblock-name:\s*([^ >]+)\s*-->", stripped
                )
                if m:
                    pending_name = m.group(1)
                continue

            # Start of fenced code block?
            if line.lstrip().startswith("```"):
                indent = len(line) - len(line.lstrip())
                m = re.match(r"^`{3,}", line.lstrip())
                if not m:
                    continue
                fence = m.group(0)
                info = line.lstrip()[len(fence):].strip()
                parts = info.split(None, 1)
                lang = parts[0].lower() if parts else ""
                extra = parts[1] if len(parts) > 1 else ""
                if lang in ("python", "py", "python3"):
                    in_block = True
                    block_indent = indent
                    start_line = idx + 1
                    code_buffer = []
                    # determine name from info string or pending comment
                    snippet_name = None
                    for token in extra.split():
                        if (
                            token.startswith("name=")
                            or token.startswith("name:")
                        ):
                            snippet_name = (
                                token.split("=", 1)[-1]
                                if "=" in token
                                else token.split(":", 1)[-1]
                            )
                            break
                    if snippet_name is None:
                        snippet_name = pending_name
                    # reset pending_name; marks stay until block closes
                    pending_name = None
                continue

        else:
            # inside a fenced code block
            if line.lstrip().startswith(fence):
                # end of block
                in_block = False
                code_text = "\n".join(code_buffer)
                snippets.append(CodeSnippet(
                    name=snippet_name,
                    code=code_text,
                    line=start_line,
                    marks=pending_marks.copy(),
                ))
                # reset pending marks after collecting
                pending_marks.clear()
                snippet_name = None
            else:
                # collect code lines (dedent by block_indent)
                if line.strip() == "":
                    code_buffer.append("")
                else:
                    if len(line) >= block_indent:
                        code_buffer.append(line[block_indent:])
                    else:
                        code_buffer.append(line.lstrip())
            continue

    return snippets


class MarkdownFile(pytest.File):
    """
    Collector for Markdown files, extracting only `test_`-prefixed code
    snippets.
    """
    def collect(self):
        text = self.fspath.read_text(encoding="utf-8")
        raw = parse_markdown(text)
        # keep only snippets named test_*
        tests = [
            sn for sn in raw if sn.name and sn.name.startswith(TEST_PREFIX)
        ]
        combined = group_snippets(tests)

        for sn in combined:
            # generate a real pytest Function so fixtures work
            if DJANGO_DB_MARKS.intersection(sn.marks):
                def make_func(code):
                    def test_block(db):
                        exec(code, {})
                    return test_block
            else:
                def make_func(code):
                    def test_block():
                        exec(code, {})
                    return test_block

            callobj = make_func(sn.code)
            fn = pytest.Function.from_parent(
                parent=self,
                name=sn.name,
                callobj=callobj,
            )
            # apply any marks (e.g. django_db)
            for m in sn.marks:
                fn.add_marker(getattr(pytest.mark, m))
            yield fn
