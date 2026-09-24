# Update version ONLY here
VERSION := 0.5.9
SHELL := /bin/bash
# Makefile for project
ROOT := $(CURDIR)
UNAME_S := $(shell uname -s)

# ----------------------------------------------------------------------------
# Documentation
# ----------------------------------------------------------------------------

# Build documentation using Sphinx and zip it
build-docs:
	uv run --extra all sphinx-source-tree
	uv run --extra all sphinx-build -n -b text docs builddocs
	uv run --extra all sphinx-build -n -a -b html docs builddocs
	cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..

rebuild-docs:
	uv run --extra all sphinx-apidoc . --full -o docs -H 'pytest-codeblock' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
	cp docs/conf.py.distrib docs/conf.py
	cp docs/index.rst.distrib docs/index.rst

build-docs-epub:
	$(MAKE) -C docs/ epub

build-docs-pdf:
	$(MAKE) -C docs/ latexpdf

auto-build-docs:
	uv run --extra all sphinx-autobuild docs docs/_build/html

# Serve the built docs on port 5001
serve-docs:
	cd builddocs && python3 -m http.server 5001

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
	uv run --extra all doc8

# Run ruff on the codebase
ruff:
	uv run --extra all ruff check .

mypy:
	uv run --extra all mypy src/pytest_codeblock/

# ----------------------------------------------------------------------------
# Installation
# ----------------------------------------------------------------------------

# Install the project (uv sync creates/updates .venv as needed)
install:
	uv sync --all-extras

# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------

# Run core tests
test: clean
	uv run --extra all pytest -vrx -s

# Run customisation tests
test-customisation: clean
	cd examples/customisation_example/ && uv run --project $(ROOT) --extra all pytest -vrx -s .

# Run nameless codeblock tests
test-nameless-codeblocks: clean
	cd examples/nameless_codeblocks_example/ && uv run --project $(ROOT) --extra all pytest -vvvrx -s .

# Run all tests
test-all:
	uv run --extra all pytest -vrx -s; \
	uv run --extra all pytest -c examples/customisation_example/pyproject.toml -vrx -s examples/customisation_example/; \
	uv run --extra all pytest -c examples/nameless_codeblocks_example/pyproject.toml -vvvrx -s examples/nameless_codeblocks_example/

# Run tests (to be used on CI environment)
test-ci: clean
	pytest -vrx -s

# Run core tests with coverage
test-cov: clean
	uv run --extra all coverage run --source=src/pytest_codeblock --omit="*/tests/*,*/conftest.py" -m pytest -vrx -s src/pytest_codeblock/tests/ -o "addopts=" -o "testpaths=src/pytest_codeblock/tests"
	uv run --extra all coverage report --omit="*/tests/*,*/conftest.py,examples/*"
	uv run --extra all coverage html --omit="*/tests/*,*/conftest.py,examples/*"

# Note: examples/*_example/ are separate uv projects (their own pyproject.toml/.venv),
# so we pin --project to the root while cwd is the example dir, keeping coverage's
# cwd-relative --source=. correct without picking up the example's own (unrelated) venv.
test-customisation-cov:
	cd examples/customisation_example/ && uv run --project $(ROOT) --extra all coverage run --source=. -m pytest -vrx -s . -o "addopts=" -o "testpaths=tests"

test-nameless-codeblocks-cov:
	cd examples/nameless_codeblocks_example/ && uv run --project $(ROOT) --extra all coverage run --source=. -m pytest -vrx -s . -o "addopts=" -o "testpaths=tests"

test-all-cov: test-cov test-customisation-cov test-nameless-codeblocks-cov

# Run tests with coverage in CI environment
test-cov-ci: clean
	coverage run --source=src/pytest_codeblock --omit="*/tests/*,*/conftest.py" -m pytest -vrx -s src/pytest_codeblock/tests/ -o "addopts=" -o "testpaths=src/pytest_codeblock/tests"
	cd examples/customisation_example/ && coverage run --source=. -m pytest -vrx -s . -o "addopts=" -o "testpaths=tests"
	cd examples/nameless_codeblocks_example/ && coverage run --source=. -m pytest -vrx -s . -o "addopts=" -o "testpaths=tests"
	coverage report --omit="*/tests/*,*/conftest.py,examples/*"
	coverage html --omit="*/tests/*,*/conftest.py,examples/*"

# ----------------------------------------------------------------------------
# Tox
# ----------------------------------------------------------------------------
# tox itself and its tox-uv plugin are run ephemerally via `uvx` — no persistent
# install step needed, and it works on a clean checkout with no prior `make install`.

# List available tox environments
tox-list:
	uvx --with tox-uv tox list

# Run all tox environments
tox:
	uvx --with tox-uv tox

# Run specific tox environment (e.g., make tox-e ENV=py312-pytest91)
tox-e:
	uvx --with tox-uv tox -e $(ENV)

# Run tox with coverage
tox-cov:
	uvx --with tox-uv tox -e py312-pytest91 -- --cov=pytest_codeblock --cov-report=html --cov-report=term

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
	rm -rf .coverage*
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf dist/
	rm -rf src/pytest_codeblock.egg-info/
	rm -rf src/pytest-codeblock.egg-info/

shell:
	uv run --extra all ipython

list-requirements:
	uv pip list

compile-requirements:
	uv pip compile --all-extras -o docs/requirements.txt pyproject.toml

compile-requirements-upgrade:
	uv pip compile --all-extras -o docs/requirements.txt pyproject.toml --upgrade

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
	uv run --extra all detect-secrets scan > .secrets.baseline

detect-secrets:
	uv run --extra all detect-secrets scan --baseline .secrets.baseline

# ----------------------------------------------------------------------------
# Release
# ----------------------------------------------------------------------------

build:
	uv run --extra all python -m build .

check-build:
	uv run --extra all twine check dist/*

release:
	uv run --extra all twine upload dist/* --verbose

test-release:
	uv run --extra all twine upload --repository testpypi dist/* --verbose

# ----------------------------------------------------------------------------
# Other
# ----------------------------------------------------------------------------

%:
	@:
