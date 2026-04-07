---
name: update-documentation
description: Sync pytest-codeblock project documentation with source code. Scans code and docs, finds misalignments, and auto-fixes them. Pure agent-based - no Python scripts involved.
---

# Update Documentation Skill

**Operation mode**: Pure agent-based documentation synchronization.

When the user asks to `sync-documentation`, the agent:
1. Scans source code to extract ground truth (pytest hooks, markers, configuration)
2. Scans all documentation files
3. Identifies misalignments between code and docs
4. **Auto-fixes documentation** to match code (reports what was changed)

**This is NOT a Python script** - the agent performs all analysis and edits directly.

## Agent-Based Sync Process

When `sync-documentation` is invoked:

### Step 1: Extract Ground Truth from Code

Scan source code to identify:

- **pytest hooks**: `pytest_collect_file`, `pytest_configure` in `src/pytest_codeblock/__init__.py` (collection phase)
- **CodeSnippet**: dataclass in `src/pytest_codeblock/collector.py` (data structure for parsed snippets)
- **RST parser**: `src/pytest_codeblock/rst.py` (parsing phase - extracts code blocks from .rst files)
- **Markdown parser**: `src/pytest_codeblock/md.py` (parsing phase - extracts code blocks from .md files)
- **Configuration options**: in `src/pytest_codeblock/config.py`
- **Markers**: in `src/pytest_codeblock/constants.py`
- **Public API**: Exports from `__all__` in `src/pytest_codeblock/__init__.py`

Note: Parsing modules (`rst.py`, `md.py`) handle extraction of code blocks from
documentation files, while pytest hooks in `__init__.py` handle collection into
pytest. When collector or fixture behavior changes, verify the parsing logic in
`rst.py` and `md.py` still produces expected `CodeSnippet` results.

### Step 2: Scan Documentation Files

Read and analyze:

- `README.rst` - Public API, quick start, usage examples
- `AGENTS.md` - Architecture, code patterns, examples
- `CONTRIBUTING.rst` - Contribution workflow
- `SECURITY.rst` - Security policy and reporting
- `docs/*.rst` - Extended documentation
- `src/pytest_codeblock/tests/tests.rst` - Documentation tests
- `src/pytest_codeblock/tests/tests.md` - Documentation tests

### Step 3: Identify Misalignments

Compare code ground truth against documentation:

- Missing pytest hooks or markers
- Undocumented configuration options
- Missing API exports
- Broken file path references
- Outdated code examples
- Missing grouping logic documentation

### Step 4: Auto-Fix Documentation

**The agent directly edits documentation files** to align with code:

- Add missing entries to tables
- Update code examples
- Fix file references
- Add missing sections
- Update configuration documentation

**SKILL.md is NOT modified** - it remains the source of truth for the skill behavior.

### Step 5: Report Changes

After fixing, report:

- Which files were modified
- What changes were made
- Any issues that couldn't be auto-fixed

---

## Documentation Files Overview

| File | Audience | Purpose |
| ---- | -------- | ------- |
| `README.rst` | End users | Public API, quick start, usage examples |
| `AGENTS.md` | AI agents | Mission, architecture, agent workflow, code patterns |
| `CONTRIBUTING.rst` | Contributors | Contribution workflow, testing, release process |
| `SECURITY.rst` | Security researchers | Security policy, reporting vulnerabilities |
| `docs/*.rst` | Users/developers | Extended documentation, API reference |
| `src/pytest_codeblock/tests/tests.rst` | Tests | Documentation tests (RST) |
| `src/pytest_codeblock/tests/tests.md` | Tests | Documentation tests (MD) |

## When to Update Each File

### README.rst

Update when:

- Public API changes (new pytest hooks, parameters)
- New configuration options
- New file formats supported
- Installation/requirement changes
- New features added

Structure to maintain:

- Features list (add new capabilities)
- Installation section
- Configuration section
- Usage examples (RST and Markdown)

### AGENTS.md

Update when:

- New parsing module added
- Collection/execution pipeline changes
- New markers or configuration options
- Testing workflow changes
- Architecture changes

Key sections:

- Project mission (never deviate: minimal deps, RST/MD support, code blocks as tests)
- Architecture table (if phases/files change)
- Development principles
- Known intentional behaviors
- Agent workflow section
- Testing rules

### CONTRIBUTING.rst

Update when:

- Contribution workflow changes
- Testing procedure changes
- Release process changes
- Code standards change

Key sections:

- Developer prerequisites
- Code standards
- Testing workflow
- Pull request process

### SECURITY.rst

Update when:

- Security policy changes
- Reporting process changes
- Supported versions change

Key sections:

- Security policy
- Supported versions
- Reporting procedure

---

## Feature-Specific Documentation Checklist

### Adding a New Marker

1. **README.rst**: Add to markers section if user-facing
2. **AGENTS.md**: Add to constants/markers documentation
3. **src/pytest_codeblock/constants.py**: Document the new marker

### Adding New Configuration Options

1. **README.rst**: Add to configuration section
2. **AGENTS.md**: Add to configuration documentation
3. **src/pytest_codeblock/config.py**: Document the new option

### Adding New Parsing Support (RST/MD)

1. **README.rst**: Add file format to features, add usage example
2. **AGENTS.md**: Update architecture table
3. **docs/restructured_text.rst** or **docs/markdown.rst**: Add detailed docs
4. **src/pytest_codeblock/tests/tests.rst** or **src/pytest_codeblock/tests/tests.md**: Add tests

### Adding New Execution Features

1. **README.rst**: Add usage example
2. **AGENTS.md**: Update execution phase description
3. **docs/*.rst**: Update relevant documentation

### Changing Default Behavior

1. **README.rst**: Update configuration defaults
2. **AGENTS.md**: Update configuration precedence
3. **All files**: Update any affected examples
4. **Changelog/docs**: Add migration notes and deprecation path

---

## Code Block Naming Convention

AGENTS.md uses executable code blocks with `name=<test_name>` attributes:

````markdown
```python name=test_example
# Code here
```

<!-- continue: test_example -->
```python name=test_example_part2
# Continues previous block, imports/vars in scope
```
````

When adding examples:

- Use descriptive names: `test_<feature>_<scenario>`
- Use `<!-- continue: <name> -->` to chain related blocks
- Ensure imports are at the top of the first block

## Documentation Standards

### RST Formatting

- Line length: 80 characters
- Use `.. code-block:: python` with `:name: test_<name>` for Python
- Use `.. code-block:: sh` for shell commands
- Use `.. note::` for callouts

### Code Examples

All code examples in AGENTS.md (and other Markdown files) should be runnable
tests. Use the `name=` attribute to prefix the block name with `test_`:

````markdown
```python name=test_feature_name
from pytest_codeblock import pytest_collect_file

# Test code here
```
````

All code examples in README.rst (and other reStructuredText files) should be
runnable tests. Use the `:name:` attribute to prefix the block name with `test_`:

```rst
.. code-block:: python
   :name: test_feature_name

   from pytest_codeblock import pytest_collect_file

   # Test code here
```

### Cross-References

- Link to related docs: ``See `CONTRIBUTING.rst`_``
- Reference other sections: ``See `Configuration`_``

## Validation Checklist

Before finishing documentation updates:

- [ ] README.rst examples match actual API
- [ ] AGENTS.md code blocks have proper `name=` attributes
- [ ] CONTRIBUTING.rst reflects current contribution process
- [ ] SECURITY.rst is up to date
- [ ] All RST files pass doc8 linting
- [ ] Cross-references between docs are valid
- [ ] File paths in docs match actual paths
- [ ] Executable code blocks in RST/MD are run and passing in pytest

## What NOT to Document

Do NOT modify documentation that is auto-generated or managed separately.

---

**Use Agent-Based Sync (`sync-documentation`) when:**
- User explicitly asks to "sync documentation"
- You need documentation auto-fixed, not just validated
- You want an interactive, conversational workflow
