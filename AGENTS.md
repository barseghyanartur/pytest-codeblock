# AGENTS.md — pytest-codeblock

**Package version**: See pyproject.toml
**Repository**: https://github.com/barseghyanartur/pytest-codeblock
**Maintainer**: Artur Barseghyan <artur.barseghyan@gmail.com>

This file is for AI agents and developers using AI assistants to work on or with
pytest-codeblock. It covers two distinct roles: **using** the plugin in
application code, and **developing/extending** the plugin itself.

---

## 1. Project Mission (Never Deviate)

> Pytest plugin to collect and test code blocks in reStructuredText and Markdown
> documentation files — ensuring docs stay correct and up-to-date.

- Code blocks are tests. Every code block in documentation is executable.
- Support both reStructuredText (``.rst``) and Markdown (``.md``) formats.
- Support code grouping across multiple blocks, async code, pytest markers,
  and pytest fixtures.
- Minimal dependencies: pytest is the only required runtime dependency.

---

## 2. Using pytest-codeblock in Application Code

### Installation

```sh
pip install pytest-codeblock
```

### Basic usage

Code blocks with names starting with ``test_`` are automatically collected and
executed as tests.

*Filename: README.rst*

```rst
.. code-block:: python
   :name: test_basic_example

   import math

   result = math.pow(3, 2)
   assert result == 9
```

*Filename: README.md*

````markdown
```python name=test_basic_example
import math

result = math.pow(3, 2)
assert result == 9
```
````

### Configuration

By default, only code blocks with names starting with ``test_`` are tested.
To test all code blocks regardless of name:

```toml
[tool.pytest-codeblock]
test_nameless_codeblocks = true
```

To customize code block identifiers and file extensions:

```toml
[tool.pytest-codeblock]
rst_user_codeblocks = ["c_py"]
rst_user_extensions = [".rst.txt"]
md_user_codeblocks = ["c_py"]
md_user_extensions = [".md.txt"]
```

### Running tests

```sh
pytest
```

Or with coverage:

```sh
pytest --cov=pytest_codeblock --cov-report=html
```

---

## 3. Architecture

The plugin works in three phases:

| Phase | File | Purpose |
| --- | --- | --- |
| **Collection** | `__init__.py` | pytest hooks: `pytest_collect_file`, `pytest_configure` |
| **Parsing** | `rst.py` / `md.py` | Extract code blocks from RST/MD files |
| **Execution** | `pytestrun.py` | Run code as pytest tests with markers/fixtures |

### Key files

| File | Purpose |
| --- | --- |
| `src/pytest_codeblock/__init__.py` | pytest entry points, marker registration |
| `src/pytest_codeblock/collector.py` | `CodeSnippet` dataclass, `group_snippets()` |
| `src/pytest_codeblock/rst.py` | reStructuredText file parsing |
| `src/pytest_codeblock/md.py` | Markdown file parsing |
| `src/pytest_codeblock/pytestrun.py` | Test execution, marker/fixture handling |
| `src/pytest_codeblock/config.py` | Configuration management |
| `src/pytest_codeblock/constants.py` | Markers, constants |
| `src/pytest_codeblock/helpers.py` | Utility functions |
| `pyproject.toml` | Build, ruff, pytest-cov configuration |
| `README.rst` | End-user documentation |

---

## 4. Development Principles

**1. Minimal dependencies.**
Only ``pytest`` is required at runtime. ``tomli`` is needed for Python 3.10.
Dev dependencies (ruff, mypy, sphinx, etc.) are optional.

**2. Backward compatibility matters.**
Public API changes require careful consideration. Deprecate rather than break.

**3. Test everything.**
All code blocks in documentation are executable tests. New features must
include documentation examples that work.

**4. Type annotations required.**
All public functions must have type annotations. Use `Optional[X]` (not
`X | None`) to match existing style.

**5. Configuration is extensible.**
Users should be able to customize code block identifiers, file extensions,
and behavior through pyproject.toml.

---

## 5. Known Intentional Behaviors — Do Not Treat as Bugs

### Nameless code blocks have grouping limitations

When `test_nameless_codeblocks = true`, code blocks without names cannot be
grouped together because there's no key to associate them. This is by design.

### Async code blocks require explicit markers

Async code blocks in documentation need the ``:ASYNC:`` mark to be executed
correctly. The parser extracts this mark and applies it to the test.

### Code block grouping modes

The `group_snippets()` function in `collector.py` operates in two modes:

- **Merge mode** (default): snippets sharing the same name are concatenated
- **Incremental mode**: when every continuation has its own distinct name,
  each step is tested in isolation with cumulative code

### Configuration precedence

Configuration is read from pyproject.toml in this order:

1. `[tool.pytest-codeblock]` section
2. Fall back to defaults in `config.py`

---

## 6. Agent Workflow: Adding Features or Fixing Bugs

When asked to add a feature or fix a bug, follow these steps in order:

1. **Understand the architecture** — Identify which phase the change affects:
   collection, parsing, or execution.
2. **For bug fixes: write a reproduction case first** — Add a test case in the
   appropriate test file that reproduces the bug. The test must fail before
   your fix.
3. **Implement the change** in the correct module:
   - Collection: `__init__.py`
   - Parsing: `rst.py` or `md.py`
   - Execution: `pytestrun.py`
   - Data structures: `collector.py`
   - Configuration: `config.py`
4. **Add/update constants** in `constants.py` if new markers or options needed
5. **Export** new public symbols from `__init__.py` and `__all__`
6. **Write tests:**
   - Unit tests in appropriate `test_*.py` files
   - Integration tests in `test_integration.py`
   - Documentation tests in `tests.rst` or `tests.md`
7. **Run linting:**

   ```sh
   make pre-commit
   ```

8. **Run tests:**

   ```sh
   make test
   make test-customisation
   make test-nameless-codeblocks
   ```

### Acceptable new features

- Support for additional documentation formats (e.g., Sphinx)
- Enhanced grouping logic for code blocks
- Additional configuration options
- Better error messages for malformed code blocks

### Forbidden

- Adding runtime dependencies beyond pytest (and tomli for py310)
- Breaking backward compatibility without deprecation period
- Removing functionality without migration path
- Writing to fixed filesystem paths (use tmp_path in tests)

---

## 7. Testing Rules

### Test structure

```text
src/pytest_codeblock/tests/
    __init__.py
    test_integration.py         — end-to-end tests
    test_pytest_codeblock.py    — core functionality tests
    test_nameless_codeblocks.py — nameless code block tests
    test_customisation.py       — configuration tests
    test_pytestrun_marker.py    — pytest marker tests
    tests.rst                   — documentation tests (RST)
    tests.md                    — documentation tests (MD)
```

### Running tests

Run all tests:

```sh
make test
make test-customisation
make test-nameless-codeblocks
```

Run with coverage:

```sh
make test-cov
make test-customisation-cov
make test-nameless-codeblocks-cov
```

Run specific test file:

```sh
pytest src/pytest_codeblock/tests/test_pytest_codeblock.py
```

### Fixture rules

- Use `tmp_path` for all filesystem operations in tests
- Create temporary RST/MD files programmatically for testing
- Never write to fixed paths

### Required assertions

- Test that code blocks are correctly collected
- Test that code blocks execute successfully
- Test that markers and fixtures are properly applied
- Test configuration options work correctly

---

## 8. Coding Conventions

Run all linting checks:

```sh
make pre-commit
```

### Formatting

- Line length: **80 characters** (ruff)
- Import sorting: `isort`; `pytest_codeblock` is `known-first-party`
- Target: Python 3.10+
- `ruff fix = true` auto-fixes on commit — do not fight the formatter

### Ruff rules in effect

`B`, `C4`, `E`, `F`, `G`, `I`, `ISC`, `INP`, `N`, `PERF`, `Q`, `SIM`, `TD`

Explicitly ignored:

| Rule | Reason |
| --- | --- |
| `G004` | f-strings in logging calls are allowed |
| `ISC003` | implicit string concatenation across lines is allowed |
| `TD002` | Missing author in TODO |
| `TD003` | Missing issue in TODO |

### Style

- Every non-test module must have `__all__`, `__author__`, `__copyright__`,
  `__license__` at module level
- Use type annotations on all public functions
- Use `Optional[X]` (not `X | None`) to match existing style

### Pull requests

Target the `dev` branch. Open PRs against `dev` for review.

---

## 9. Prompt Templates

**Explaining usage to a user:**
> You are an expert in pytest plugin development. Explain how to use
> pytest-codeblock to test documentation code blocks. Cover installation,
> basic usage with RST and Markdown, configuration options, and how to run
> the tests. Mention the difference between named code blocks (test_*) and
> nameless code blocks.

**Implementing a new feature:**
> Extend pytest-codeblock with [feature]. Follow the AGENTS.md agent workflow
> (section 6): identify the correct phase, implement, add tests, update
> documentation. Preserve minimal dependencies and backward compatibility.

**Fixing a bug:**
> Reproduce [bug] with a new test case. The test must fail before the fix.
> Then fix in the correct module. Add tests asserting the correct behavior
> and verify existing functionality still works.

**Reviewing a change:**
> Review this pytest-codeblock change against AGENTS.md: Does it maintain
> minimal dependencies? Does it follow the architecture (collection/parsing/
> execution)? Are all new features tested? Is backward compatibility preserved?
