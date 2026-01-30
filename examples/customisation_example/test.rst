test.rst
========

test_rst_python_hello
---------------------
.. code-block:: python
    :name: test_rst_python_hello

    import math

    result = math.pow(3, 2)
    assert result == 9
    print(f"Hello test.rst: {result}")

test_rst_c_py_hello
-------------------

.. code-block:: c_py
    :name: test_rst_c_py_hello

    import math

    result = math.pow(2, 2)
    assert result == 4
    print(f"Hello test.rst: {result}")
