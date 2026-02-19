"""Tests for pytestrun marker functionality."""


class TestPytestrunMarker:
    """Test pytestrun marker handling in pytest-codeblock."""

    # -------------------------------------------------------------------------

    def test_pytestrun_with_class_fixtures(self, pytester_subprocess):
        """Test pytestrun marker with class-level fixtures."""
        pytester_subprocess.makefile(
            ".md",
            test_pytestrun="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_class_fixtures
import pytest

class TestSystemInfo:

    @pytest.fixture
    def system_name(self):
        return "Linux"

    @pytest.fixture
    def version_number(self):
        return 5

    def test_combined_info(self, system_name, version_number):
        info = f"{system_name} v{version_number}"
        assert info == "Linux v5"

    def test_name_only(self, system_name):
        assert system_name.isalpha()
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=2)

    # -------------------------------------------------------------------------

    def test_pytestrun_with_conftest_fixtures(self, pytester_subprocess):
        """Test pytestrun marker with conftest fixtures."""
        pytester_subprocess.makefile(
            ".md",
            test_pytestrun_conftest="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_conftest_fixtures
import pytest

class TestSystemInfo:

    def test_request(self, http_request):
        assert isinstance(http_request.GET, dict)
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    # -------------------------------------------------------------------------

    def test_pytestrun_with_setup_teardown(self, pytester_subprocess):
        """Test pytestrun marker with setup_method."""
        pytester_subprocess.makefile(
            ".md",
            test_pytestrun_setup="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_setup_teardown
import pytest

class TestWithSetup:

    def setup_method(self):
        self.value = 10

    def test_value_set(self):
        assert self.value == 10

    def test_value_modified(self):
        self.value += 5
        assert self.value == 15
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=2)

    def test_pytestrun_with_parametrize(self, pytester_subprocess):
        """Test pytestrun marker with parametrize."""
        pytester_subprocess.makefile(
            ".md",
            test_pytestrun_param="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_parametrize
import pytest

class TestParametrized:

    @pytest.mark.parametrize("input,expected", [(1, 2), (3, 4)])
    def test_increment(self, input, expected):
        assert input + 1 == expected
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=2)

    # -------------------------------------------------------------------------

    def test_pytestrun_nested_fixtures(self, pytester_subprocess):
        """Test pytestrun marker with nested fixtures."""
        pytester_subprocess.makefile(
            ".md",
            test_pytestrun_nested="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_nested_fixtures
import pytest

class TestNestedFixtures:

    @pytest.fixture
    def base_value(self):
        return 100

    @pytest.fixture
    def derived_value(self, base_value):
        return base_value * 2

    def test_derived(self, derived_value):
        assert derived_value == 200
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    # -------------------------------------------------------------------------

    def test_pytestrun_mixed_fixtures(self, pytester_subprocess):
        """Test pytestrun marker with both conftest and class fixtures."""
        pytester_subprocess.makefile(
            ".md",
            test_pytestrun_mixed="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_mixed_fixtures
import pytest

class TestMixedFixtures:

    @pytest.fixture
    def local_data(self):
        return {"key": "value"}

    def test_both_fixtures(self, http_request, local_data):
        assert isinstance(http_request.GET, dict)
        assert local_data["key"] == "value"
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=1)

    # -------------------------------------------------------------------------

    def test_pytestrun_multiple_methods(self, pytester_subprocess):
        """Test pytestrun marker with multiple test methods."""
        pytester_subprocess.makefile(
            ".md",
            test_pytestrun_multi="""
<!-- pytestmark: pytestrun -->
```python name=test_pytestrun_multiple_methods
import pytest

class TestMultipleMethods:

    @pytest.fixture
    def shared_list(self):
        return [1, 2, 3]

    def test_length(self, shared_list):
        assert len(shared_list) == 3

    def test_first_element(self, shared_list):
        assert shared_list[0] == 1

    def test_sum(self, shared_list):
        assert sum(shared_list) == 6
```
""",
        )
        result = pytester_subprocess.runpytest("-v", "-p", "no:django")
        result.assert_outcomes(passed=3)
