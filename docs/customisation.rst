Customisation
=============

It's possible to customise which codeblock languages and file extensions
are recognised by the plugin.

----

Languages
---------
By default, the plugin recognises the following codeblock languages:

- reStructuredText: `python`, `py`, `python3`
- Markdown: `python`, `py`, `python3`

reStructruredText
~~~~~~~~~~~~~~~~~

For reStructruredText defaults are configured via `rst_codeblocks` setting in
the `[tool.pytest-codeblock]` section of your `pyproject.toml`.

.. code-block:: toml

    [tool.pytest-codeblock]
    rst_codeblocks = ["python", "py", "python3"]

.. note::

    Don't touch the defaults, unless you want to remove certain options.

If you only want to add custom codeblock languages, use `rst_user_codeblocks`.

The following example adds `c_py` as a custom codeblock language:

.. code-block:: toml

    [tool.pytest-codeblock]
    rst_user_codeblocks = ["c_py"]

Now the following codeblock will be recognised and executed:

.. code-block:: rst

    .. code-block:: c_py
       :name: test_c_py_example

       print("This is a custom Python codeblock")

Markdown
~~~~~~~~

For Markdown defaults configured via `md_codeblocks` setting in
the `[tool.pytest-codeblock]` section of your `pyproject.toml`.

.. code-block:: toml

    [tool.pytest-codeblock]
    md_codeblocks = ["python", "py", "python3"]

.. note::

    Don't touch the defaults, unless you want to remove certain options.

If you only want to add custom codeblock languages, use `md_user_codeblocks`.

The following example adds `c_py` as a custom codeblock language:

.. code-block:: toml

    [tool.pytest-codeblock]
    md_user_codeblocks = ["c_py"]

Now the following codeblock will be recognised and executed:

.. code-block:: markdown

    ```c_py name=test_c_py_example
    print("This is a custom Python codeblock")
    ```

----

Extensions
----------

.. note::
    
    If you customise both reStructuredText and Markdown configurations,
    make sure to avoid overlapping file extensions.

reStructruredText
~~~~~~~~~~~~~~~~~

By default, the plugin recognises the following file extensions for 
reStructuredText files: `.rst`

These defaults are configured via `rst_extensions` setting in
the `[tool.pytest-codeblock]` section of your `pyproject.toml`.

.. code-block:: toml

    [tool.pytest-codeblock]
    rst_extensions = [".rst"]

.. note::

    Don't touch the defaults, unless you want to remove certain options.

If you only want to add custom file extensions, use `rst_user_extensions`. 

The following example adds `.rst.txt` as a custom reStructuredText file 
extension:

.. code-block:: toml

    [tool.pytest-codeblock]
    rst_user_extensions = [".rst.txt"]

Now the following file will be recognised and processed:

.. code-block:: rst

    *Filename: example.rst.txt*

    .. code-block:: python
       :name: test_custom_rst_extension_example

       print("Custom .rst.txt extension example executed successfully!")

Markdown
~~~~~~~~

By default, the plugin recognises the following file extensions for 
Markdown files: `.md`, `.markdown`, `.mdx`

These defaults are configured via `md_extensions` setting in
the `[tool.pytest-codeblock]` section of your `pyproject.toml`.

.. code-block:: toml

    [tool.pytest-codeblock]
    md_extensions = [".md", ".markdown", ".mdx"]

.. note::

    Don't touch the defaults, unless you want to remove certain options.

If you only want to add custom file extensions, use `md_user_extensions`.

The following example adds `.md.txt` as a custom Markdown file extension:

.. code-block:: toml

    [tool.pytest-codeblock]
    md_user_extensions = [".md.txt"]

Now the following file will be recognised and processed:

.. code-block:: markdown

    *Filename: example.md.txt*

    ```python name=test_custom_md_extension_example
    print("Custom .md.txt extension example executed successfully!")
    ```

----

MDX
---

`MDX <https://mdxjs.com>`__ files (``.mdx``) are Markdown with JSX. They are collected by
default and parsed by the Markdown parser. No configuration is needed.

The following file will be recognised and processed:

.. code-block:: markdown

    *Filename: example.mdx*

    import { Callout } from './callout'

    <Callout type="info">JSX is ignored by the plugin.</Callout>

    ```python name=test_custom_mdx_extension_example
    print("Custom .mdx extension example executed successfully!")
    ```

MDX does not allow HTML comments, so write directives as JSX comments
instead:

.. code-block:: markdown

    {/* pytestmark: xfail */}
    ```python name=test_mdx_xfail_example
    assert False
    ```

The same applies to the ``pytestfixture``, ``continue`` and
``codeblock-name`` directives. Both comment forms work in ``.md`` and
``.mdx`` files.

.. note::

    The plugin reads ``.mdx`` files line by line and does not understand
    JSX. A fenced code block inside a JSX expression, such as a template
    literal or a component prop, is still collected and executed.

To stop collecting ``.mdx`` files, leave the extension out of
`md_extensions`:

.. code-block:: toml

    [tool.pytest-codeblock]
    md_extensions = [".md", ".markdown"]

See ``examples/mdx_example/`` in the repository for a complete example.
