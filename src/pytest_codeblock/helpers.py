import ast
import textwrap

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "contains_top_level_await",
    "wrap_async_code",
)


def contains_top_level_await(code: str) -> bool:
    """Analyzes code to detect presence of async patterns."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # If the code is invalid, it technically doesn't
        # contain valid async patterns.
        return False

    # Define the AST nodes that represent async constructs
    async_nodes = (
        ast.AsyncFunctionDef,  # async def ...
        ast.Await,  # await ...
        ast.AsyncWith,  # async with ...
        ast.AsyncFor,  # async for ...
    )

    return any(isinstance(node, async_nodes) for node in ast.walk(tree))


def wrap_async_code(code: str) -> str:
    """Wrap code containing top-level await in an async function."""
    ind = textwrap.indent(code, "    ")
    return (
        f"async def __async_main__():\n{ind}\n\nasyncio.run(__async_main__())"
    )
