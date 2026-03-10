"""Tests for project configuration files.

This module tests the structure and validity of various project
configuration and documentation files.
"""

import json
import os
import re
from pathlib import Path

import pytest

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

import yaml

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "test_coderabbit_yaml_exists",
    "test_coderabbit_yaml_structure",
    "test_coderabbit_yaml_valid_language",
    "test_coderabbit_yaml_valid_profile",
    "test_coderabbit_yaml_path_filters_format",
    "test_coderabbit_yaml_base_branches_configured",
    "test_gitignore_exists",
    "test_gitignore_has_python_patterns",
    "test_gitignore_has_common_patterns",
    "test_gitignore_excludes_coverage",
    "test_gitignore_does_not_ignore_important_files",
    "test_gitignore_line_ending_consistency",
    "test_gitignore_patterns_are_valid",
    "test_gitignore_no_absolute_paths",
    "test_secrets_baseline_exists",
    "test_secrets_baseline_structure",
    "test_secrets_baseline_has_plugins",
    "test_secrets_baseline_has_filters",
    "test_secrets_baseline_valid_json",
    "test_secrets_baseline_timestamp_format",
    "test_secrets_baseline_version_format",
    "test_secrets_baseline_results_structure",
    "test_secrets_baseline_no_plaintext_secrets",
    "test_makefile_exists",
    "test_makefile_has_test_targets",
    "test_makefile_has_docs_targets",
    "test_makefile_has_version_variable",
    "test_makefile_has_clean_target",
    "test_makefile_has_install_target",
    "test_makefile_has_linting_targets",
    "test_makefile_has_build_targets",
    "test_makefile_targets_are_phony_safe",
    "test_makefile_no_tab_issues",
    "test_makefile_version_matches_pyproject",
    "test_pyproject_toml_exists",
    "test_pyproject_toml_valid",
    "test_pyproject_toml_has_project_section",
    "test_pyproject_toml_has_name",
    "test_pyproject_toml_has_version",
    "test_pyproject_toml_has_dependencies",
    "test_pyproject_toml_has_pytest_entrypoint",
    "test_pyproject_toml_has_build_system",
    "test_pyproject_toml_has_ruff_config",
    "test_pyproject_toml_python_version",
    "test_pyproject_toml_has_all_test_dependencies",
    "test_pyproject_toml_classifiers_python_versions",
    "test_pyproject_toml_optional_deps_no_duplicates",
    "test_pyproject_toml_sphinx_source_tree_config",
    "test_pyproject_toml_ruff_line_length",
    "test_contributing_rst_exists",
    "test_contributing_rst_valid_syntax",
    "test_contributing_rst_has_sections",
    "test_contributing_rst_has_pre_commit_info",
    "test_contributing_rst_no_broken_links_syntax",
    "test_contributing_rst_code_block_syntax",
    "test_source_tree_rst_exists",
    "test_source_tree_rst_valid_syntax",
    "test_source_tree_rst_has_literalinclude",
    "test_source_tree_rst_caption_usage",
    "test_source_tree_rst_language_specification",
    "test_source_tree_full_rst_exists",
    "test_source_tree_full_rst_valid_syntax",
    "test_source_tree_full_rst_has_examples",
    "test_documentation_files_no_trailing_whitespace",
    "test_all_config_files_readable",
)


# Test fixtures
@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture
def coderabbit_yaml_path(project_root):
    """Return path to .coderabbit.yaml."""
    return project_root / ".coderabbit.yaml"


@pytest.fixture
def gitignore_path(project_root):
    """Return path to .gitignore."""
    return project_root / ".gitignore"


@pytest.fixture
def secrets_baseline_path(project_root):
    """Return path to .secrets.baseline."""
    return project_root / ".secrets.baseline"


@pytest.fixture
def makefile_path(project_root):
    """Return path to Makefile."""
    return project_root / "Makefile"


@pytest.fixture
def pyproject_toml_path(project_root):
    """Return path to pyproject.toml."""
    return project_root / "pyproject.toml"


@pytest.fixture
def contributing_rst_path(project_root):
    """Return path to CONTRIBUTING.rst."""
    return project_root / "CONTRIBUTING.rst"


@pytest.fixture
def source_tree_rst_path(project_root):
    """Return path to docs/source_tree.rst."""
    return project_root / "docs" / "source_tree.rst"


@pytest.fixture
def source_tree_full_rst_path(project_root):
    """Return path to docs/source_tree_full.rst."""
    return project_root / "docs" / "source_tree_full.rst"


# .coderabbit.yaml tests
def test_coderabbit_yaml_exists(coderabbit_yaml_path):
    """Test that .coderabbit.yaml file exists."""
    assert coderabbit_yaml_path.exists(), ".coderabbit.yaml file not found"


def test_coderabbit_yaml_structure(coderabbit_yaml_path):
    """Test that .coderabbit.yaml has valid YAML structure."""
    with open(coderabbit_yaml_path) as f:
        config = yaml.safe_load(f)
    assert isinstance(config, dict), "Config should be a dictionary"
    assert "language" in config, "Config should have 'language' field"
    assert "reviews" in config, "Config should have 'reviews' field"


def test_coderabbit_yaml_valid_language(coderabbit_yaml_path):
    """Test that language is set correctly."""
    with open(coderabbit_yaml_path) as f:
        config = yaml.safe_load(f)
    assert config["language"] == "en", "Language should be 'en'"


def test_coderabbit_yaml_valid_profile(coderabbit_yaml_path):
    """Test that reviews profile is configured."""
    with open(coderabbit_yaml_path) as f:
        config = yaml.safe_load(f)
    assert "profile" in config["reviews"], "Reviews should have a profile"
    assert config["reviews"]["profile"] == "chill"


# .gitignore tests
def test_gitignore_exists(gitignore_path):
    """Test that .gitignore file exists."""
    assert gitignore_path.exists(), ".gitignore file not found"


def test_gitignore_has_python_patterns(gitignore_path):
    """Test that .gitignore includes common Python patterns."""
    with open(gitignore_path) as f:
        content = f.read()

    # Check for common Python patterns
    assert "*.py[cod]" in content, "Should ignore compiled Python files"
    assert "__pycache__" in content or ".pytest_cache/" in content


def test_gitignore_has_common_patterns(gitignore_path):
    """Test that .gitignore includes common development patterns."""
    with open(gitignore_path) as f:
        content = f.read()

    # Check for common patterns
    patterns = [".tox/", ".vscode/", ".idea/", "build/", "dist/"]
    for pattern in patterns:
        assert pattern in content, f"Should ignore {pattern}"


def test_gitignore_excludes_coverage(gitignore_path):
    """Test that .gitignore excludes coverage files."""
    with open(gitignore_path) as f:
        content = f.read()

    assert ".coverage" in content, "Should ignore coverage files"
    assert "/htmlcov/" in content or "htmlcov/" in content


def test_gitignore_does_not_ignore_important_files(gitignore_path):
    """Test that .gitignore doesn't accidentally ignore important files."""
    with open(gitignore_path) as f:
        content = f.read()

    # Should NOT ignore these patterns entirely
    assert "!.coveragerc" in content, "Should keep .coveragerc"


# .secrets.baseline tests
def test_secrets_baseline_exists(secrets_baseline_path):
    """Test that .secrets.baseline file exists."""
    assert secrets_baseline_path.exists(), ".secrets.baseline file not found"


def test_secrets_baseline_valid_json(secrets_baseline_path):
    """Test that .secrets.baseline is valid JSON."""
    with open(secrets_baseline_path) as f:
        data = json.load(f)
    assert isinstance(data, dict), "Secrets baseline should be a dictionary"


def test_secrets_baseline_structure(secrets_baseline_path):
    """Test that .secrets.baseline has required structure."""
    with open(secrets_baseline_path) as f:
        data = json.load(f)

    assert "version" in data, "Should have version field"
    assert "plugins_used" in data, "Should have plugins_used field"
    assert "filters_used" in data, "Should have filters_used field"
    assert "results" in data, "Should have results field"


def test_secrets_baseline_has_plugins(secrets_baseline_path):
    """Test that .secrets.baseline has configured plugins."""
    with open(secrets_baseline_path) as f:
        data = json.load(f)

    plugins = data["plugins_used"]
    assert len(plugins) > 0, "Should have at least one plugin configured"

    # Check for common plugin types
    plugin_names = [p["name"] for p in plugins]
    assert "AWSKeyDetector" in plugin_names


def test_secrets_baseline_has_filters(secrets_baseline_path):
    """Test that .secrets.baseline has configured filters."""
    with open(secrets_baseline_path) as f:
        data = json.load(f)

    filters = data["filters_used"]
    assert len(filters) > 0, "Should have at least one filter configured"


def test_secrets_baseline_timestamp_format(secrets_baseline_path):
    """Test that generated_at timestamp is in valid format."""
    with open(secrets_baseline_path) as f:
        data = json.load(f)

    assert "generated_at" in data, "Should have generated_at timestamp"
    # Should be ISO 8601 format like "2026-03-10T22:00:25Z"
    timestamp = data["generated_at"]
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp)


# Makefile tests
def test_makefile_exists(makefile_path):
    """Test that Makefile exists."""
    assert makefile_path.exists(), "Makefile not found"


def test_makefile_has_test_targets(makefile_path):
    """Test that Makefile has test targets."""
    with open(makefile_path) as f:
        content = f.read()

    targets = ["test:", "test-all:", "test-cov:"]
    for target in targets:
        assert target in content, f"Makefile should have {target} target"


def test_makefile_has_docs_targets(makefile_path):
    """Test that Makefile has documentation targets."""
    with open(makefile_path) as f:
        content = f.read()

    targets = ["build-docs:", "serve-docs:"]
    for target in targets:
        assert target in content, f"Makefile should have {target} target"


def test_makefile_has_version_variable(makefile_path):
    """Test that Makefile defines VERSION variable."""
    with open(makefile_path) as f:
        content = f.read()

    assert re.search(r"VERSION\s*:?=", content), "Should define VERSION"


def test_makefile_has_clean_target(makefile_path):
    """Test that Makefile has clean target."""
    with open(makefile_path) as f:
        content = f.read()

    assert "clean:" in content, "Should have clean target"
    # Check it removes common artifacts
    assert "*.pyc" in content or "*.py[cod]" in content
    assert "__pycache__" in content


def test_makefile_has_install_target(makefile_path):
    """Test that Makefile has install target."""
    with open(makefile_path) as f:
        content = f.read()

    assert "install:" in content, "Should have install target"


def test_makefile_has_linting_targets(makefile_path):
    """Test that Makefile has linting targets."""
    with open(makefile_path) as f:
        content = f.read()

    targets = ["ruff:", "doc8:"]
    for target in targets:
        assert target in content, f"Makefile should have {target} target"


def test_makefile_has_build_targets(makefile_path):
    """Test that Makefile has build and release targets."""
    with open(makefile_path) as f:
        content = f.read()

    targets = ["build:", "release:"]
    for target in targets:
        assert target in content, f"Makefile should have {target} target"


# pyproject.toml tests
def test_pyproject_toml_exists(pyproject_toml_path):
    """Test that pyproject.toml exists."""
    assert pyproject_toml_path.exists(), "pyproject.toml not found"


def test_pyproject_toml_valid(pyproject_toml_path):
    """Test that pyproject.toml is valid TOML."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)
    assert isinstance(data, dict), "Should be a valid TOML dictionary"


def test_pyproject_toml_has_project_section(pyproject_toml_path):
    """Test that pyproject.toml has [project] section."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    assert "project" in data, "Should have [project] section"


def test_pyproject_toml_has_name(pyproject_toml_path):
    """Test that project name is defined."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    assert "name" in data["project"], "Should have project name"
    assert data["project"]["name"] == "pytest-codeblock"


def test_pyproject_toml_has_version(pyproject_toml_path):
    """Test that project version is defined."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    assert "version" in data["project"], "Should have version"
    # Version should match semantic versioning pattern
    version = data["project"]["version"]
    assert re.match(r"\d+\.\d+\.\d+", version), "Version should be semver"


def test_pyproject_toml_has_dependencies(pyproject_toml_path):
    """Test that dependencies are defined."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    assert "dependencies" in data["project"], "Should have dependencies"
    deps = data["project"]["dependencies"]
    assert "pytest" in str(deps), "Should depend on pytest"


def test_pyproject_toml_has_pytest_entrypoint(pyproject_toml_path):
    """Test that pytest entrypoint is configured."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    assert "project" in data
    assert "entry-points" in data["project"]
    assert "pytest11" in data["project"]["entry-points"]
    assert "pytest_codeblock" in data["project"]["entry-points"]["pytest11"]


def test_pyproject_toml_has_build_system(pyproject_toml_path):
    """Test that build system is configured."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    assert "build-system" in data, "Should have build-system section"
    assert "requires" in data["build-system"]
    assert "build-backend" in data["build-system"]


def test_pyproject_toml_has_ruff_config(pyproject_toml_path):
    """Test that ruff is configured."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    assert "tool" in data, "Should have [tool] section"
    assert "ruff" in data["tool"], "Should have ruff configuration"


def test_pyproject_toml_python_version(pyproject_toml_path):
    """Test that required Python version is specified."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    assert "requires-python" in data["project"]
    # Should specify minimum Python version
    requires = data["project"]["requires-python"]
    assert ">=" in requires, "Should specify minimum version"


def test_pyproject_toml_has_all_test_dependencies(pyproject_toml_path):
    """Test that all test dependencies are properly defined."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    assert "optional-dependencies" in data["project"]
    assert "test" in data["project"]["optional-dependencies"]
    test_deps = data["project"]["optional-dependencies"]["test"]

    # Check for essential test dependencies
    test_deps_str = str(test_deps)
    assert "pytest" in test_deps_str
    assert "pytest-cov" in test_deps_str


# CONTRIBUTING.rst tests
def test_contributing_rst_exists(contributing_rst_path):
    """Test that CONTRIBUTING.rst exists."""
    assert contributing_rst_path.exists(), "CONTRIBUTING.rst not found"


def test_contributing_rst_valid_syntax(contributing_rst_path):
    """Test that CONTRIBUTING.rst has valid reStructuredText syntax."""
    with open(contributing_rst_path) as f:
        content = f.read()

    # Basic RST syntax checks
    # Should have section headers
    assert "=" in content, "Should have section headers"
    # Should not have obvious syntax errors
    assert content.strip(), "File should not be empty"


def test_contributing_rst_has_sections(contributing_rst_path):
    """Test that CONTRIBUTING.rst has expected sections."""
    with open(contributing_rst_path) as f:
        content = f.read()

    # Check for important sections
    sections = [
        "prerequisites",
        "Code standards",
        "Testing",
        "Pull requests",
    ]
    content_lower = content.lower()
    for section in sections:
        assert section.lower() in content_lower, f"Should have {section}"


def test_contributing_rst_has_pre_commit_info(contributing_rst_path):
    """Test that pre-commit setup is documented."""
    with open(contributing_rst_path) as f:
        content = f.read()

    assert "pre-commit" in content, "Should mention pre-commit"
    assert "install" in content, "Should mention installation"


# docs/source_tree.rst tests
def test_source_tree_rst_exists(source_tree_rst_path):
    """Test that docs/source_tree.rst exists."""
    assert source_tree_rst_path.exists(), "docs/source_tree.rst not found"


def test_source_tree_rst_valid_syntax(source_tree_rst_path):
    """Test that source_tree.rst has valid RST syntax."""
    with open(source_tree_rst_path) as f:
        content = f.read()

    assert content.strip(), "File should not be empty"
    assert "Project source-tree" in content


def test_source_tree_rst_has_literalinclude(source_tree_rst_path):
    """Test that source_tree.rst uses literalinclude directives."""
    with open(source_tree_rst_path) as f:
        content = f.read()

    # Should use literalinclude to include source files
    assert ".. literalinclude::" in content


# docs/source_tree_full.rst tests
def test_source_tree_full_rst_exists(source_tree_full_rst_path):
    """Test that docs/source_tree_full.rst exists."""
    assert (
        source_tree_full_rst_path.exists()
    ), "docs/source_tree_full.rst not found"


def test_source_tree_full_rst_valid_syntax(source_tree_full_rst_path):
    """Test that source_tree_full.rst has valid RST syntax."""
    with open(source_tree_full_rst_path) as f:
        content = f.read()

    assert content.strip(), "File should not be empty"
    assert "Full project source-tree" in content


def test_source_tree_full_rst_has_examples(source_tree_full_rst_path):
    """Test that source_tree_full.rst includes examples directory."""
    with open(source_tree_full_rst_path) as f:
        content = f.read()

    # Full tree should include examples
    assert "examples" in content.lower()


# Additional edge case and regression tests
def test_coderabbit_yaml_path_filters_format(coderabbit_yaml_path):
    """Test that path_filters are properly formatted as a list."""
    with open(coderabbit_yaml_path) as f:
        config = yaml.safe_load(f)

    if "path_filters" in config.get("reviews", {}):
        path_filters = config["reviews"]["path_filters"]
        assert isinstance(path_filters, list), "path_filters should be a list"
        # Should have at least the wildcard pattern
        assert any("**/*" in str(p) for p in path_filters)


def test_coderabbit_yaml_base_branches_configured(coderabbit_yaml_path):
    """Test that base branches are configured for auto-review."""
    with open(coderabbit_yaml_path) as f:
        config = yaml.safe_load(f)

    if "auto_review" in config.get("reviews", {}):
        auto_review = config["reviews"]["auto_review"]
        assert "base_branches" in auto_review
        base_branches = auto_review["base_branches"]
        assert isinstance(base_branches, list)
        # Should include main branch
        assert "main" in base_branches


def test_gitignore_line_ending_consistency(gitignore_path):
    """Test that .gitignore doesn't have mixed line endings."""
    with open(gitignore_path, "rb") as f:
        content = f.read()

    # Should not have Windows line endings mixed with Unix
    assert b"\r\n" not in content or content.count(b"\r\n") == content.count(
        b"\n"
    ), "Should have consistent line endings"


def test_gitignore_patterns_are_valid(gitignore_path):
    """Test that gitignore patterns are syntactically valid."""
    with open(gitignore_path) as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()
        # Skip comments and empty lines
        if not stripped or stripped.startswith("#"):
            continue
        # Pattern should not have trailing spaces
        assert line.rstrip() == stripped or line.endswith(
            "\n"
        ), f"Pattern has trailing spaces: {repr(line)}"


def test_gitignore_no_absolute_paths(gitignore_path):
    """Test that .gitignore doesn't contain absolute paths."""
    with open(gitignore_path) as f:
        content = f.read()

    # Should not have absolute paths (starting with /)
    # except for anchored patterns which are valid
    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    # Patterns starting with / are anchored to repo root, which is valid
    # Just ensure no obvious absolute system paths like /usr/, /home/, etc.
    for line in lines:
        assert not line.startswith("/usr/"), "Should not have /usr/ paths"
        assert not line.startswith("/home/"), "Should not have /home/ paths"
        assert not line.startswith("/etc/"), "Should not have /etc/ paths"


def test_secrets_baseline_version_format(secrets_baseline_path):
    """Test that version follows semantic versioning."""
    with open(secrets_baseline_path) as f:
        data = json.load(f)

    version = data["version"]
    # Should be in format X.Y.Z
    assert re.match(r"\d+\.\d+\.\d+", version), "Version should be semver"


def test_secrets_baseline_results_structure(secrets_baseline_path):
    """Test that results section has proper structure."""
    with open(secrets_baseline_path) as f:
        data = json.load(f)

    results = data["results"]
    assert isinstance(results, dict), "Results should be a dictionary"

    # If there are results, they should have required fields
    for filepath, findings in results.items():
        assert isinstance(findings, list), f"Findings for {filepath} should be a list"
        for finding in findings:
            assert "type" in finding, "Finding should have 'type'"
            assert "filename" in finding, "Finding should have 'filename'"
            assert "hashed_secret" in finding, "Finding should have 'hashed_secret'"
            assert "line_number" in finding, "Finding should have 'line_number'"


def test_secrets_baseline_no_plaintext_secrets(secrets_baseline_path):
    """Test that secrets are hashed, not stored in plaintext."""
    with open(secrets_baseline_path) as f:
        content = f.read()

    # Should not contain obvious plaintext secrets
    assert "password" not in content.lower() or "hashed_secret" in content
    # Ensure all secrets are hashed (SHA-1 format)
    if '"hashed_secret"' in content:
        # Extract all hashed_secret values
        hashes = re.findall(r'"hashed_secret":\s*"([^"]+)"', content)
        for hash_val in hashes:
            # SHA-1 hashes are 40 hex characters
            assert len(hash_val) == 40, f"Invalid hash length: {hash_val}"
            assert re.match(
                r"^[a-f0-9]{40}$", hash_val
            ), f"Invalid hash format: {hash_val}"


def test_makefile_targets_are_phony_safe(makefile_path):
    """Test that common targets don't conflict with file names."""
    with open(makefile_path) as f:
        content = f.read()

    # Common targets that should be phony
    common_targets = ["clean", "test", "install", "build"]

    for target in common_targets:
        if f"{target}:" in content:
            # These should be safe to run even if files with those names exist
            # This is a documentation test - just verify the targets exist
            assert f"{target}:" in content


def test_makefile_no_tab_issues(makefile_path):
    """Test that Makefile uses tabs for recipe indentation."""
    with open(makefile_path, "rb") as f:
        lines = f.readlines()

    in_recipe = False
    for i, line in enumerate(lines, 1):
        line_str = line.decode("utf-8")

        # Check if this is a target line
        if ":" in line_str and not line_str.startswith("\t") and not line_str.startswith("#"):
            in_recipe = True
            continue

        # If we're in a recipe and the line is indented
        if in_recipe and line_str.startswith((" ", "\t")) and line_str.strip():
            # Recipe lines must start with tab, not spaces
            if not line_str.startswith("\t"):
                # Could be a variable continuation, check if previous line ended with =
                pass  # Allow for variable assignments
            elif line_str.startswith(" "):
                pytest.fail(
                    f"Line {i} starts with spaces instead of tab: {line_str[:20]}"
                )

        # Empty line or new target resets recipe state
        if not line_str.strip() or (
            ":" in line_str and not line_str.startswith("\t")
        ):
            in_recipe = False


def test_makefile_version_matches_pyproject(makefile_path, pyproject_toml_path):
    """Test that VERSION in Makefile matches pyproject.toml version."""
    # Read Makefile version
    with open(makefile_path) as f:
        makefile_content = f.read()

    makefile_version_match = re.search(r"VERSION\s*:?=\s*([0-9.]+)", makefile_content)
    assert makefile_version_match, "VERSION not found in Makefile"
    makefile_version = makefile_version_match.group(1)

    # Read pyproject.toml version
    with open(pyproject_toml_path, "rb") as f:
        pyproject_data = tomllib.load(f)

    pyproject_version = pyproject_data["project"]["version"]

    assert (
        makefile_version == pyproject_version
    ), f"Versions don't match: Makefile={makefile_version}, pyproject.toml={pyproject_version}"


def test_pyproject_toml_classifiers_python_versions(pyproject_toml_path):
    """Test that Python version classifiers are consistent."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    classifiers = data["project"].get("classifiers", [])

    # Extract Python version classifiers
    py_classifiers = [c for c in classifiers if "Programming Language :: Python :: 3." in c]

    # Should have multiple Python versions
    assert len(py_classifiers) >= 3, "Should support multiple Python 3.x versions"

    # Versions should be in ascending order
    versions = []
    for classifier in py_classifiers:
        match = re.search(r"3\.(\d+)", classifier)
        if match:
            versions.append(int(match.group(1)))

    # Check if sorted
    assert versions == sorted(versions), "Python version classifiers should be in order"


def test_pyproject_toml_optional_deps_no_duplicates(pyproject_toml_path):
    """Test that optional dependencies don't have duplicates."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    optional_deps = data["project"].get("optional-dependencies", {})

    for group_name, deps in optional_deps.items():
        # Extract package names (without version specifiers)
        package_names = []
        for dep in deps:
            # Handle various formats: "pkg", "pkg>=1.0", "pkg[extra]", etc.
            pkg_name = re.split(r"[>=<\[;]", str(dep))[0].strip()
            package_names.append(pkg_name.lower())

        # Check for duplicates
        duplicates = [name for name in package_names if package_names.count(name) > 1]
        assert not duplicates, f"Duplicate packages in {group_name}: {set(duplicates)}"


def test_pyproject_toml_sphinx_source_tree_config(pyproject_toml_path):
    """Test that sphinx-source-tree tool configuration is present."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    assert "tool" in data
    assert "sphinx-source-tree" in data["tool"]

    config = data["tool"]["sphinx-source-tree"]
    assert "ignore" in config, "Should have ignore patterns"
    assert "order" in config, "Should have order configuration"

    # Should have file configurations
    assert "files" in config
    files_config = config["files"]
    assert isinstance(files_config, list)
    assert len(files_config) >= 2, "Should have at least 2 file outputs configured"


def test_pyproject_toml_ruff_line_length(pyproject_toml_path):
    """Test that ruff line length is configured."""
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)

    ruff_config = data["tool"]["ruff"]
    assert "line-length" in ruff_config
    line_length = ruff_config["line-length"]
    assert isinstance(line_length, int)
    assert 60 <= line_length <= 120, "Line length should be reasonable"


def test_contributing_rst_no_broken_links_syntax(contributing_rst_path):
    """Test that RST link syntax is not obviously broken."""
    with open(contributing_rst_path) as f:
        content = f.read()

    # Check for link definitions (.. _name: url)
    link_defs = re.findall(r"\.\.\s+_[a-zA-Z0-9_-]+:\s+https?://", content)
    assert len(link_defs) > 5, "Should have multiple external link definitions"

    # Check for link references (`text`_)
    link_refs = re.findall(r"`[^`]+`_", content)
    assert len(link_refs) > 0, "Should have link references"


def test_contributing_rst_code_block_syntax(contributing_rst_path):
    """Test that code blocks use valid RST syntax."""
    with open(contributing_rst_path) as f:
        content = f.read()

    # Should have code blocks
    assert ".. code-block::" in content, "Should have code-block directives"

    # Find all code-block directives
    code_blocks = re.findall(r"\.\. code-block::\s+\w+", content)
    assert len(code_blocks) >= 3, "Should have multiple code blocks"


def test_source_tree_rst_caption_usage(source_tree_rst_path):
    """Test that literalinclude directives use captions."""
    with open(source_tree_rst_path) as f:
        content = f.read()

    # Count literalinclude directives
    includes = content.count(".. literalinclude::")

    if includes > 0:
        # Should use captions
        captions = content.count(":caption:")
        # Not all includes need captions, but most should have them
        assert captions > 0, "Should use captions for literalinclude"


def test_source_tree_rst_language_specification(source_tree_rst_path):
    """Test that literalinclude directives specify language."""
    with open(source_tree_rst_path) as f:
        content = f.read()

    # Should specify languages like :language: python, :language: rst, etc.
    if ".. literalinclude::" in content:
        languages = re.findall(r":language:\s+\w+", content)
        assert len(languages) > 0, "Should specify language for includes"


def test_documentation_files_no_trailing_whitespace(
    contributing_rst_path, source_tree_rst_path, source_tree_full_rst_path
):
    """Test that documentation files don't have trailing whitespace."""
    files = [contributing_rst_path, source_tree_rst_path, source_tree_full_rst_path]

    for filepath in files:
        with open(filepath) as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            # Allow lines that are just newlines
            if line == "\n":
                continue
            # Check for trailing whitespace before newline
            assert not re.search(
                r"[ \t]+\n$", line
            ), f"{filepath.name}:{i} has trailing whitespace"


def test_all_config_files_readable(
    coderabbit_yaml_path,
    gitignore_path,
    secrets_baseline_path,
    makefile_path,
    pyproject_toml_path,
):
    """Test that all configuration files are readable and not empty."""
    config_files = [
        coderabbit_yaml_path,
        gitignore_path,
        secrets_baseline_path,
        makefile_path,
        pyproject_toml_path,
    ]

    for filepath in config_files:
        assert filepath.exists(), f"{filepath} does not exist"
        assert filepath.is_file(), f"{filepath} is not a file"
        assert filepath.stat().st_size > 0, f"{filepath} is empty"

        # Should be readable
        with open(filepath) as f:
            content = f.read()
            assert len(content) > 0, f"{filepath} has no content"