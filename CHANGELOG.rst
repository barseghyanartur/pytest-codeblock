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
