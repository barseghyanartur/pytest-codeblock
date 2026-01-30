import asyncio
import inspect
import re
import textwrap
import traceback
from typing import Optional

import pytest

from .collector import CodeSnippet, group_snippets
from .config import get_config
from .constants import CODEBLOCK_MARK, DJANGO_DB_MARKS, TEST_PREFIX
from .helpers import contains_top_level_await, wrap_async_code

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
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
      - <!-- continue: <name> --> comments for grouping with a named snippet
      - Fenced code blocks with ```python (and optional name=<name> in the
        info string)

    Captures each snippet's name, code, starting line, and any pytest marks.
    """
    config = get_config()
    snippets: list[CodeSnippet] = []
    lines = text.splitlines()
    pending_name: Optional[str] = None
    pending_continue: Optional[str] = None
    pending_marks: list[str] = [CODEBLOCK_MARK]
    pending_fixtures: list[str] = []
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

            # Check for pytest fixture comment
            if stripped.startswith("<!--") and "pytestfixture:" in stripped:
                m = re.match(r"<!--\s*pytestfixture:\s*(\w+)\s*-->", stripped)
                if m:
                    pending_fixtures.append(m.group(1))
                continue

            # Check for continue comment
            if stripped.startswith("<!--") and "continue:" in stripped:
                m = re.match(r"<!--\s*continue:\s*(\S+)\s*-->", stripped)
                if m:
                    pending_continue = m.group(1)
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
                if lang in config.all_md_codeblocks:
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
                # continue overrides snippet_name for grouping
                if pending_continue:
                    final_name = pending_continue
                    pending_continue = None
                else:
                    final_name = snippet_name
                snippets.append(CodeSnippet(
                    name=final_name,
                    code=code_text,
                    line=start_line,
                    marks=pending_marks.copy(),
                    fixtures=pending_fixtures.copy(),
                ))
                # reset pending marks after collecting
                pending_marks = [CODEBLOCK_MARK]  # Reset to default
                snippet_name = None
                pending_fixtures.clear()  # Clear pending fixtures
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
        text = self.path.read_text(encoding="utf-8")
        raw = parse_markdown(text)
        # keep only snippets named test_*
        tests = [
            sn for sn in raw if sn.name and sn.name.startswith(TEST_PREFIX)
        ]
        combined = group_snippets(tests)

        for sn in combined:
            # Bind the values we need so we don't close over `sn` itself
            _sn_name = sn.name
            _fpath = str(self.path)

            # Build list of fixture names requested by this snippet
            _fixture_names: list[str] = list(sn.fixtures)

            # If snippet is marked as needing DB, also request the `db`
            # fixture, unless user already added it explicitly.
            if (
                DJANGO_DB_MARKS.intersection(sn.marks)
                and "db" not in _fixture_names
            ):
                _fixture_names.append("db")

            # Generate a real pytest Function so fixtures work
            def make_func(
                code,
                sn_name=_sn_name,
                fpath=_fpath,
                fixture_names=_fixture_names,
            ):
                # This inner function *actually* has a **fixtures signature,
                # but we override __signature__ so pytest passes the right
                # fixtures and names.
                def test_block(**fixtures):
                    # Auto-wrap async code
                    ex_code = code
                    if contains_top_level_await(code):
                        ex_code = wrap_async_code(code)

                    try:
                        compiled = compile(ex_code, fpath, "exec")
                    except SyntaxError as err:
                        raise SyntaxError(
                            f"Syntax error in "
                            f"codeblock `{sn_name}` in {fpath}:\n"
                            f"\n{textwrap.indent(ex_code, prefix='    ')}\n\n"
                            f"{traceback.format_exc()}"
                        ) from err

                    try:
                        # Make fixtures available as top-level names
                        # inside the executed snippet.
                        exec(compiled, {"asyncio": asyncio, **dict(fixtures)})
                    except Exception as err:
                        raise Exception(
                            f"Error in "
                            f"codeblock `{sn_name}` in {fpath}:\n"
                            f"\n{textwrap.indent(ex_code, prefix='    ')}\n\n"
                            f"{traceback.format_exc()}"
                        ) from err

                # Tell pytest which fixture arguments this test has:
                test_block.__signature__ = inspect.Signature(
                    [
                        inspect.Parameter(
                            name,
                            inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        )
                        for name in fixture_names
                    ]
                )
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
