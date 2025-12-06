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
