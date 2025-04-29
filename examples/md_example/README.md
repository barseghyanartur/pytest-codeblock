# Markdown example project

This is a minimal example showing how pytest-codeblock will discover and run
only Python snippets whose `name` starts with test_.

## Simple assertion

```python name=test_simple_assert
# A trivial test that always passes
assert 2 + 2 == 4
```

## Multi-part example

It's possible to split one logical test into multiple blocks. All of them
share the same ``name``:

```python name=test_compute_square
import math
```

Some intervening text.

```python name=test_compute_square
result = math.pow(3, 2)
assert result == 9
```

Some intervening text.

```python name=test_compute_square
print(result)
```

## Ignored snippets

Blocks without a `name` or without the `test_` prefix are **not** collected:

```python name=example_not_test
# Name does not start with `test_`, so this is ignored
```

## Non-Python blocks are also ignored

```bash name=test_should_be_ignored
echo "Not Python → skipped"
```

## Custom pytest marks

<!-- pytestmark: django_db -->
```python name=test_django
from django.contrib.auth.models import User

user = User.objects.first()
```
