test.rst
========

test_named_codeblock
---------------------
.. code-block:: python
    :name: test_named_codeblock

    import math

    result = math.pow(3, 2)
    assert result == 9
    print(f"Hello test.rst: {result}")

test_nameless_codeblock_1
-------------------------

.. code-block:: python

    import math

    result = math.pow(2, 2)
    assert result == 4
    print(f"Hello test.rst: {result}")

test_nameless_codeblock_2
-------------------------

.. code-block:: python

    import math

    result = math.pow(2, 3)
    assert result == 8
    print(f"Hello test.rst: {result}")
