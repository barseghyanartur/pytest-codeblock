# Requesting pytest-fixtures

pytest-fixtures examples.

## External references

- [pytest-fixtures](https://docs.pytest.org/en/6.2.x/fixture.html)

## `pytest-fixtures` example

<!-- pytestfixture: tmp_path -->
<!-- pytestfixture: http_request -->
```python name=test_path_and_http_request
d = tmp_path / "sub"
d.mkdir()  # Create the directory
assert d.is_dir()  # Verify it was created and is a directory

assert isinstance(http_request.GET, dict)
```
