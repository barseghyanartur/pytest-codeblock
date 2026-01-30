Customisation
=============

It's possible to customise which codeblock languages and file extensions
are recognised by the plugin.

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

The following example adds `djc_py` as a custom codeblock language:

.. code-block:: toml

    [tool.pytest-codeblock]
    rst_user_codeblocks = ["djc_py"]

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

The following example adds `djc_py` as a custom codeblock language:

.. code-block:: toml

    [tool.pytest-codeblock]
    md_user_codeblocks = ["djc_py"]

Extensions
----------

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

The following example adds `.rest` as a custom reStructuredText file extension:

.. code-block:: toml

    [tool.pytest-codeblock]
    rst_user_extensions = [".rest"]

Markdown
~~~~~~~~

By default, the plugin recognises the following file extensions for 
Markdown files: `.md`, `.markdown`

These defaults are configured via `md_extensions` setting in
the `[tool.pytest-codeblock]` section of your `pyproject.toml`.

.. code-block:: toml

    [tool.pytest-codeblock]
    md_extensions = [".md", ".markdown"]

.. note::

    Don't touch the defaults, unless you want to remove certain options.

If you only want to add custom file extensions, use `md_user_extensions`.

The following example adds `.mdown` as a custom Markdown file extension:

.. code-block:: toml

    [tool.pytest-codeblock]
    md_user_extensions = [".mdown"]

