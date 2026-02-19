# Update version ONLY here
VERSION := 0.5.4
SHELL := /bin/bash
# Makefile for project
VENV := .venv/bin/activate
UNAME_S := $(shell uname -s)

# ----------------------------------------------------------------------------
# Documentation
# ----------------------------------------------------------------------------

# Build documentation using Sphinx and zip it
build-docs:
	source $(VENV) && sphinx-source-tree
	source $(VENV) && sphinx-build -n -b text docs builddocs
	source $(VENV) && sphinx-build -n -a -b html docs builddocs
	cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..

rebuild-docs:
	source $(VENV) && sphinx-apidoc . --full -o docs -H 'pytest-codeblock' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
	cp docs/conf.py.distrib docs/conf.py
	cp docs/index.rst.distrib docs/index.rst

build-docs-epub:
	$(MAKE) -C docs/ epub

build-docs-pdf:
	$(MAKE) -C docs/ latexpdf

auto-build-docs:
	source $(VENV) && sphinx-autobuild docs docs/_build/html

# Serve the built docs on port 5001
serve-docs:
	source $(VENV) && cd builddocs && python -m http.server 5001

# ----------------------------------------------------------------------------
# Pre-commit
# ----------------------------------------------------------------------------

pre-commit-install:
	pre-commit install

pre-commit: pre-commit-install
	pre-commit run --all-files

# ----------------------------------------------------------------------------
# Linting
# ----------------------------------------------------------------------------

pyupgrade:
	pre-commit run --all-files pyupgrade

doc8:
	source $(VENV) && doc8

# Run ruff on the codebase
ruff:
	source $(VENV) && ruff check .

mypy:
	source $(VENV) && mypy src/pytest_codeblock/

# ----------------------------------------------------------------------------
# Installation
# ----------------------------------------------------------------------------

create-venv:
	uv venv

# Install the project
install: create-venv
	source $(VENV) && uv pip install -e .[all]

# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------

# Run core tests
test: clean
	source $(VENV) && pytest -vrx -s

# Run customisation tests
test-customisation: clean
	source $(VENV) && cd examples/customisation_example/ && pytest -vrx -s

# Run nameless codeblock tests
test-nameless-codeblocks: clean
	source $(VENV) && cd examples/nameless_codeblocks_example/ && pytest -vvvrx -s

# Run all tests
test-all: test test-customisation test-nameless-codeblocks

# Run tests (to be used on CI environment)
test-ci: clean
	pytest -vrx -s

# Run core tests with coverage
test-cov: clean
	source $(VENV) && coverage run --source=src/pytest_codeblock --omit="*/tests/*,*/conftest.py" -m pytest -vrx -s src/pytest_codeblock/tests/ -o "addopts=" -o "testpaths=src/pytest_codeblock/tests"
	source $(VENV) && coverage report --omit="*/tests/*,*/conftest.py,examples/*"
	source $(VENV) && coverage html --omit="*/tests/*,*/conftest.py,examples/*"

test-customisation-cov:
	source $(VENV) && cd examples/customisation_example/ && coverage run --source=. -m pytest -vrx -s . -o "addopts=" -o "testpaths=tests"

test-nameless-codeblocks-cov:
	source $(VENV) && cd examples/nameless_codeblocks_example/ && coverage run --source=. -m pytest -vrx -s . -o "addopts=" -o "testpaths=tests"

test-all-cov: test-cov test-customisation-cov test-nameless-codeblocks-cov

# Run tests with coverage in CI environment
test-cov-ci: clean
	coverage run --source=src/pytest_codeblock --omit="*/tests/*,*/conftest.py" -m pytest -vrx -s src/pytest_codeblock/tests/ -o "addopts=" -o "testpaths=src/pytest_codeblock/tests"
	cd examples/customisation_example/ && coverage run --source=. -m pytest -vrx -s . -o "addopts=" -o "testpaths=tests"
	cd examples/nameless_codeblocks_example/ && coverage run --source=. -m pytest -vrx -s . -o "addopts=" -o "testpaths=tests"
	coverage report --omit="*/tests/*,*/conftest.py,examples/*"
	coverage html --omit="*/tests/*,*/conftest.py,examples/*"

# ----------------------------------------------------------------------------
# Development
# ----------------------------------------------------------------------------

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -exec rm -f {} \;
	find . -type f -name "builddocs.zip" -exec rm -f {} \;
	find . -type f -name "*.py,cover" -exec rm -f {} \;
	find . -type f -name "*.orig" -exec rm -f {} \;
	find . -type f -name "*.coverage" -exec rm -f {} \;
	find . -type f -name "*.db" -exec rm -f {} \;
	find . -type d -name "__pycache__" -exec rm -rf {} \; -prune
	rm -rf build/
	rm -rf dist/
	rm -rf .cache/
	rm -rf htmlcov/
	rm -rf examples/customisation_example/htmlcov/
	rm -rf src/pytest_codeblock/tests/htmlcov/
	rm -rf builddocs/
	rm -rf testdocs/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf dist/
	rm -rf src/pytest_codeblock.egg-info/
	rm -rf src/pytest-codeblock.egg-info/

shell:
	source $(VENV) && ipython

compile-requirements:
	source $(VENV) && uv pip compile --all-extras -o docs/requirements.txt pyproject.toml

compile-requirements-upgrade:
	source $(VENV) && uv pip compile --all-extras -o docs/requirements.txt pyproject.toml --upgrade

update-version:
	@echo "Updating version in pyproject.toml and __init__.py"
	@if [ "$(UNAME_S)" = "Darwin" ]; then \
		gsed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml; \
		gsed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' src/pytest_codeblock/__init__.py; \
	else \
		sed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml; \
		sed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' src/pytest_codeblock/__init__.py; \
	fi

# ----------------------------------------------------------------------------
# Security
# ----------------------------------------------------------------------------

create-secrets:
	source $(VENV) && detect-secrets scan > .secrets.baseline

detect-secrets:
	source $(VENV) && detect-secrets scan --baseline .secrets.baseline

# ----------------------------------------------------------------------------
# Release
# ----------------------------------------------------------------------------

build:
	source $(VENV) && python -m build .

check-build:
	source $(VENV) && twine check dist/*

release:
	source $(VENV) && twine upload dist/* --verbose

test-release:
	source $(VENV) && twine upload --repository testpypi dist/* --verbose

# ----------------------------------------------------------------------------
# Other
# ----------------------------------------------------------------------------

%:
	@:
