__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "CODEBLOCK_MARK",
    "DJANGO_DB_MARKS",
    "PYTESTRUN_MARK",
    "TEST_PREFIX",
)

DJANGO_DB_MARKS = {
    "django_db",
    "db",
    "transactional_db",
}

TEST_PREFIX = "test_"

CODEBLOCK_MARK = "codeblock"

# When this mark is present on a code block, the plugin will exec() the block
# and then discover and run any Test* classes / test_* functions found in it,
# rather than treating the whole block as a single test body.
PYTESTRUN_MARK = "pytestrun"
