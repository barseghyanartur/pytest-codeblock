# test.md

## test_named_codeblock
```python name=test_named_codeblock
import math

result = math.pow(3, 2)
assert result == 9
print(f"Hello test.md: {result}")
```

## test_nameless_codeblock_1
```python
import math

result = math.pow(2, 2)
assert result == 4
print(f"Hello test.md: {result}")
```

## test_nameless_codeblock_2
```python
import math

result = math.pow(2, 3)
assert result == 8
print(f"Hello test.md: {result}")
```

## test_nameless_codeblock_3

<!-- pytestmark: xfail -->
```python
assert False
```

## test_nameless_codeblock_4

<!-- pytestfixture: tmp_path -->

```python
# Use the tmp_path fixture in your test
file_path = tmp_path / "example.txt"
file_path.write_text("Hello, World!")
assert file_path.read_text() == "Hello, World!"
```

## test_nameless_codeblock_5

```python name=test_named_codeblock_2
x = 1
```

Some text.

<!-- continue: test_named_codeblock_2 -->
```python
y = x + 1  # Uses x from the first snippet
assert y == 2
print(f"Hello test.md: {y}")
```
