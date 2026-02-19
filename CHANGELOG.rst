Release history and notes
=========================
.. Internal references

.. _Armenian genocide: https://en.wikipedia.org/wiki/Armenian_genocide

`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It is always safe to upgrade within the same minor version (for example,
  from 0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.5.4
-----
2026-02-19

- Fixes in ``pytestrun`` marker functionality. Allow all custom ``pytest``
  definitions (from conftest.py) inside code blocks with ``pytestrun``
  marker.

0.5.3
-----
2026-02-18

- Add a new ``pytestrun`` marker, which allows code blocks in
  reStructuredText and Markdown to be executed as standalone pytest suites.
  Unlike standard code blocks that are simply executed with `exec()`,
  blocks with ``pytestrun`` marker are written to a temporary file and run
  via a subprocess using ``pytest``. This enables full support for test
  classes, fixtures, and setup/teardown within documentation snippets.
  The implementation also adds auto-registration for the ``pytestrun`` marker
  and ensures the subprocess inherits the current ``PYTHONPATH`` for proper
  module discovery.

0.5.2
-----
2026-02-16

- Fix recently introduced bug when only first block in ``.rst`` file
  had ``codeblock`` mark.
- Automatically register the ``codeblock`` marker to prevent pytest warnings
  or errors in strict configurations when the marker isn't manually defined.

0.5.1
-----
2026-02-12

- Minor documentation improvements.

0.5
---
2026-02-08

- Allow code blocks without names. By default, this option is disabled and
  code blocks without names are ignored. To enable it,
  set ``test_nameless_codeblocks`` to ``true`` in your pyproject.toml
  configuration.

0.4
---
2026-01-30

- Add customisation support for codeblock languages in both reStructuredText
  and Markdown files.
- Add customisation support for file extensions in both reStructuredText
  and Markdown files.
- Stop testing against 3.9. Minimum supported version is now Python 3.10.

0.3.5
-----
2026-01-29

- Add more tests. Improved test coverage.

0.3.4
-----
2026-01-21

- Add new syntax for grouping multiple code blocks in markdown files.
- Add more tests to tests.md and tests.rst files for markup specific testing.

0.3.3
-----
2026-01-20

- Minor code and documentation fixes.
- Add a dedicated tests.md file for markdown specific testing.

0.3.2
-----
2026-01-19

- Add support for `async` in code blocks.

0.3.1
-----
2025-12-06

- Test against Python 3.14.
- Add sphinx-llms-txt-link integration.

0.3
---
2025-11-26

.. note::

    Release is dedicated to my beloved son Rafayel. Happy birthday!

- Make it possible to request pytest-fixtures.

0.2
---
2025-11-15

- Handle deprecations for pytest 9.x. The ``fspath`` argument is replaced with
  ``path`` and the code is updated accordingly.

0.1.8
-----
2025-05-11

- Move everything to `src` directory.
- Add Python tests.

0.1.7
-----
2025-05-11

- Minor fixes.

0.1.6
-----
2025-05-10

- Minor fixes.

0.1.5
-----
2025-05-07

- Improve error tracebacks.

0.1.4
-----
2025-05-05

- Fixes in `.. literalinclude` blocks.

0.1.3
-----
2025-05-05

- Add support for `.. literalinclude` blocks.

0.1.2
-----
2025-05-03

- Automatically add `codeblock` mark to documentation tests.
- Add customisation section to documentation.

0.1.1
-----
2025-04-30

- Support Python 3.9.

0.1
---
2025-04-29

.. note::

    In memory of the victims of the
    `Armenian Genocide <https://en.wikipedia.org/wiki/Armenian_genocide>`_.

- Initial beta release.
