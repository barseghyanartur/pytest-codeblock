from pytest_codeblock.collector import CodeSnippet, group_snippets
from pytest_codeblock.md import parse_markdown
from pytest_codeblock.rst import (
    get_literalinclude_content,
    parse_rst,
    resolve_literalinclude_path,
)


def test_group_snippets_merges_named():
    # Two snippets with the same name should be combined
    sn1 = CodeSnippet(name="foo", code="a=1", line=1, marks=["codeblock"])
    sn2 = CodeSnippet(name="foo", code="b=2", line=2, marks=["codeblock", "m"])
    combined = group_snippets([sn1, sn2])
    assert len(combined) == 1
    cs = combined[0]
    assert cs.name == "foo"
    # Both code parts should appear
    assert "a=1" in cs.code
    assert "b=2" in cs.code
    # Marks should accumulate
    assert "m" in cs.marks


def test_group_snippets_different_names():
    # Snippets with different names are not grouped
    sn1 = CodeSnippet(name="foo", code="x=1", line=1)
    sn2 = CodeSnippet(name="bar", code="y=2", line=2)
    combined = group_snippets([sn1, sn2])
    assert len(combined) == 2
    assert combined[0].name.startswith("foo")
    assert combined[1].name.startswith("bar")


def test_parse_markdown_simple():
    text = """
```python name=test_example
x=1
assert x==1
```"""
    snippets = parse_markdown(text)
    assert len(snippets) == 1
    sn = snippets[0]
    assert sn.name == "test_example"
    assert "x=1" in sn.code


def test_parse_markdown_with_pytestmark():
    text = """
<!-- pytestmark: django_db -->
```python name=test_db
from django.db import models
```"""
    snippets = parse_markdown(text)
    assert len(snippets) == 1
    sn = snippets[0]
    # Should include both default and django_db marks
    assert "django_db" in sn.marks
    assert "codeblock" in sn.marks


def test_resolve_literalinclude_and_content(tmp_path):
    base = tmp_path / "dir"
    base.mkdir()
    file = base / "a.py"
    file.write_text("print('hello')")
    # Absolute path resolution
    abs_path = resolve_literalinclude_path(base, str(file))
    assert abs_path == str(file.resolve())
    # Relative path resolution
    rel_path = resolve_literalinclude_path(base, "a.py")
    assert rel_path == str(file.resolve())
    # Content read
    content = get_literalinclude_content(str(file))
    assert content == "print('hello')"


def test_parse_rst_simple(tmp_path):
    # Basic code-block directive
    rst = """
.. code-block:: python
   :name: test_simple

   a=2
   assert a==2
"""
    snippets = parse_rst(rst, tmp_path)
    assert len(snippets) == 1
    sn = snippets[0]
    assert sn.name == "test_simple"
    assert "a=2" in sn.code


def test_parse_rst_literalinclude(tmp_path):
    # Create an external file to include
    include_dir = tmp_path / "inc"
    include_dir.mkdir()
    target = include_dir / "foo.py"
    target.write_text("z=3\nassert z==3")
    rst = f"""
.. literalinclude:: {target.name}
   :name: test_li
"""
    snippets = parse_rst(rst, include_dir)
    assert len(snippets) == 1
    sn = snippets[0]
    assert sn.name == "test_li"
    assert "z=3" in sn.code
