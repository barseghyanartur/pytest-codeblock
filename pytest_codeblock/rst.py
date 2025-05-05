import re
from pathlib import Path
from typing import Optional

import pytest

from .collector import CodeSnippet, group_snippets
from .constants import CODEBLOCK_MARK, DJANGO_DB_MARKS, TEST_PREFIX

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "RSTFile",
    "parse_rst",
)

# Highlight: Added helper function for literalinclude path resolution
def resolve_literalinclude_path(
    base_dir: Path,
    include_path: str,
) -> Optional[str]:
    """
    Resolve the full path for a literalinclude directive.
    Returns None if the file doesn't exist.
    """
    _include_path = Path(include_path)
    if _include_path.exists():
        return str(_include_path.resolve())

    try:
        full_path = base_dir / include_path
        if full_path.exists():
            return str(full_path.resolve())
    except Exception:
        pass
    return None


def get_literalinclude_content(path):
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(
            f"Failed to read literalinclude file {path}: {e}"
        ) from e


def parse_rst(text: str, base_dir: Path) -> list[CodeSnippet]:
    """
    Parse an RST document into CodeSnippet objects, capturing:
      - .. pytestmark: <mark>
      - .. continue: <name>
      - .. codeblock-name: <name>
      - .. code-block:: python
    """
    snippets: list[CodeSnippet] = []
    lines = text.splitlines()
    n = len(lines)

    pending_name: Optional[str] = None
    pending_marks: list[str] = [CODEBLOCK_MARK]
    pending_continue: Optional[str] = None
    i = 0

    while i < n:
        line = lines[i]

        # --------------------------------------------------------------------
        # Collect `.. pytestmark: xyz`
        # --------------------------------------------------------------------
        m = re.match(r"^\s*\.\.\s*pytestmark:\s*(\w+)\s*$", line)
        if m:
            pending_marks.append(m.group(1))
            i += 1
            continue

        # --------------------------------------------------------------------
        # The `.. literalinclude` directive
        # --------------------------------------------------------------------
        if line.strip().startswith(".. literalinclude::"):
            path = line.split(".. literalinclude::", 1)[1].strip()
            name = None

            # Look ahead for name
            j = i + 1
            while j < len(lines) and lines[j].strip():
                if ":name:" in lines[j]:
                    name = lines[j].split(":name:", 1)[1].strip()
                    break
                j += 1

            if name and name.startswith("test_"):
                full_path = resolve_literalinclude_path(base_dir, path)
                if full_path:
                    snippet = CodeSnippet(
                        code=get_literalinclude_content(full_path),
                        line=i + 1,
                        name=name,
                        marks=pending_marks.copy(),
                    )
                    snippets.append(snippet)

            i = j + 1
            continue

        # --------------------------------------------------------------------
        # Collect `.. continue: foo`
        # --------------------------------------------------------------------
        m = re.match(r"^\s*\.\.\s*continue:\s*(\S+)\s*$", line)
        if m:
            pending_continue = m.group(1)
            i += 1
            continue

        # --------------------------------------------------------------------
        # Collect `.. codeblock-name: foo`
        # --------------------------------------------------------------------
        m = re.match(r"^\s*\.\.\s*codeblock-name:\s*(\S+)\s*$", line)
        if m:
            pending_name = m.group(1)
            i += 1
            continue

        # --------------------------------------------------------------------
        # The `.. code-block` directive
        # --------------------------------------------------------------------
        m = re.match(r"^(\s*)\.\. (?:code-block|code)::\s*(\w+)", line)
        if m:
            base_indent = len(m.group(1))
            lang = m.group(2).lower()
            if lang in ("python", "py", "python3"):
                # Parse :name: option
                name_val: Optional[str] = None
                j = i + 1
                while j < n:
                    ln = lines[j]
                    if not ln.strip():
                        j += 1
                        continue
                    indent = len(ln) - len(ln.lstrip())
                    if ln.lstrip().startswith(":") and indent > base_indent:
                        opt = ln.lstrip()
                        if opt.lower().startswith(":name:"):
                            name_val = opt.split(":", 2)[2].strip().split()[0]
                        j += 1
                        continue
                    break
                # The j is first code line
                if j >= n:
                    i = j
                    continue
                first = lines[j]
                content_indent = len(first) - len(first.lstrip())
                if content_indent <= base_indent:
                    i = j
                    continue
                # Collect code
                buf: list[str] = []
                k = j
                while k < n:
                    ln = lines[k]
                    if not ln.strip():
                        buf.append("")
                        k += 1
                        continue
                    ind = len(ln) - len(ln.lstrip())
                    if ind >= content_indent:
                        buf.append(ln[content_indent:])
                        k += 1
                    else:
                        break
                # Decide snippet name: continue overrides name_val/pending_name
                if pending_continue:
                    sn_name = pending_continue
                    pending_continue = None
                else:
                    sn_name = name_val or pending_name
                sn_marks = pending_marks.copy()
                pending_name = None
                pending_marks.clear()

                snippets.append(CodeSnippet(
                    name=sn_name,
                    code="\n".join(buf),
                    line=j + 1,
                    marks=sn_marks,
                ))

                i = k
                continue
            else:
                i += 1
                continue

        # --------------------------------------------------------------------
        # The literal-block via "::"
        # --------------------------------------------------------------------
        if line.rstrip().endswith("::") and pending_name:
            # Similar override logic
            if pending_continue:
                sn_name = pending_continue
                pending_continue = None
            else:
                sn_name = pending_name
            sn_marks = pending_marks.copy()
            pending_name = None
            pending_marks.clear()
            j = i + 1
            if j < n and not lines[j].strip():
                j += 1
            if j >= n:
                i = j
                continue
            first = lines[j]
            content_indent = len(first) - len(first.lstrip())
            buf: list[str] = []
            k = j
            while k < n:
                ln = lines[k]
                if not ln.strip():
                    buf.append("")
                    k += 1
                    continue
                ind = len(ln) - len(ln.lstrip())
                if ind >= content_indent:
                    buf.append(ln[content_indent:])
                    k += 1
                else:
                    break
            snippets.append(CodeSnippet(
                name=sn_name,
                code="\n".join(buf),
                line=j + 1,
                marks=sn_marks,
            ))
            i = k
            continue

        i += 1

    return snippets


class RSTFile(pytest.File):
    """Collect RST code-block tests as real test functions."""
    def collect(self):
        text = self.fspath.read_text(encoding="utf-8")
        raw = parse_rst(text, self.fspath)

        # Only keep test_* snippets
        tests = [
            sn for sn in raw if sn.name and sn.name.startswith(TEST_PREFIX)
        ]
        combined = group_snippets(tests)

        for sn in combined:
            # Create a Python function for this snippet
            if DJANGO_DB_MARKS.intersection(sn.marks):
                # Function *requests* the db fixture
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
                callobj=callobj
            )
            # Re-apply any pytest.mark.<foo> markers
            for m in sn.marks:
                fn.add_marker(getattr(pytest.mark, m))
            yield fn
