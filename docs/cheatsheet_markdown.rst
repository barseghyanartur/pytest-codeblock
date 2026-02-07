Markdown cheatsheet
===================
This cheatsheet provides a quick reference to some of the most commonly used 
features and commands.

Marking code-block as xfailed
-----------------------------

To mark a code-block as expected to fail (xfailed), use the following syntax:

.. code-block:: markdown

    <! -- pytestmark: xfail -->
    ```python name=test_example_xfail

    # Normally this test would fail, but it will xfail instead
    assert False
    ```

Requesting specific pytest fixtures for a code-block
----------------------------------------------------
To request specific pytest fixtures for a code-block, use the following syntax:

.. code-block:: markdown

    <!-- pytestfixture: tmp_path -->
    ```python name=test_example_with_fixtures
    # Use the tmp_path fixture in your test
    file_path = tmp_path / "example.txt"
    file_path.write_text("Hello, World!")
    assert file_path.read_text() == "Hello, World!"
    ```
