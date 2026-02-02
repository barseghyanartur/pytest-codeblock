Cheatsheet
==========
This cheatsheet provides a quick reference to some of the most commonly used 
features and commands.

Marking example as xfailed
---------------------------

To mark a test example as expected to fail (xfailed), use the following syntax:

.. code-block:: rst

    .. pytestmark: xfail
    .. code-block:: python
        :name: test_example_xfail

        # Normally this test would fail, but it will xfail instead
        assert False
