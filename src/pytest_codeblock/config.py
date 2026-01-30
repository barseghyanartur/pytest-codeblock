"""Configuration loading from pyproject.toml."""
import sys
from pathlib import Path
from typing import Optional

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore[assignment]

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "get_config",
    "Config",
)

# Default values
DEFAULT_RST_CODEBLOCKS = ("py", "python", "python3")
DEFAULT_MD_CODEBLOCKS = ("py", "python", "python3")
DEFAULT_RST_EXTENSIONS = (".rst",)
DEFAULT_MD_EXTENSIONS = (".md", ".markdown")


class Config:
    """Configuration container for pytest-codeblock."""

    def __init__(
        self,
        rst_codeblocks: tuple[str, ...] = DEFAULT_RST_CODEBLOCKS,
        rst_user_codeblocks: tuple[str, ...] = (),
        md_codeblocks: tuple[str, ...] = DEFAULT_MD_CODEBLOCKS,
        md_user_codeblocks: tuple[str, ...] = (),
        rst_extensions: tuple[str, ...] = DEFAULT_RST_EXTENSIONS,
        rst_user_extensions: tuple[str, ...] = (),
        md_extensions: tuple[str, ...] = DEFAULT_MD_EXTENSIONS,
        md_user_extensions: tuple[str, ...] = (),
    ):
        self.rst_codeblocks = rst_codeblocks
        self.rst_user_codeblocks = rst_user_codeblocks
        self.md_codeblocks = md_codeblocks
        self.md_user_codeblocks = md_user_codeblocks
        self.rst_extensions = rst_extensions
        self.rst_user_extensions = rst_user_extensions
        self.md_extensions = md_extensions
        self.md_user_extensions = md_user_extensions

    @property
    def all_rst_codeblocks(self) -> tuple[str, ...]:
        """Combined RST codeblocks (system + user)."""
        return self.rst_codeblocks + self.rst_user_codeblocks

    @property
    def all_md_codeblocks(self) -> tuple[str, ...]:
        """Combined MD codeblocks (system + user)."""
        return self.md_codeblocks + self.md_user_codeblocks

    @property
    def all_rst_extensions(self) -> tuple[str, ...]:
        """Combined RST extensions (system + user)."""
        return self.rst_extensions + self.rst_user_extensions

    @property
    def all_md_extensions(self) -> tuple[str, ...]:
        """Combined MD extensions (system + user)."""
        return self.md_extensions + self.md_user_extensions


_cached_config: Optional[Config] = None


def _find_pyproject_toml() -> Optional[Path]:
    """Find pyproject.toml starting from cwd and going up."""
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / "pyproject.toml"
        if candidate.is_file():
            return candidate
    return None


def _load_config_from_pyproject(path: Path) -> dict:
    """Load [tool.pytest-codeblock] section from pyproject.toml."""
    if tomllib is None:
        return {}
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
        return data.get("tool", {}).get("pytest-codeblock", {})
    except Exception:
        return {}


def get_config(*, force_reload: bool = False) -> Config:
    """Get the configuration, loading from pyproject.toml if available."""
    global _cached_config

    if _cached_config is not None and not force_reload:
        return _cached_config

    pyproject_path = _find_pyproject_toml()
    if pyproject_path is None:
        _cached_config = Config()
        return _cached_config

    raw = _load_config_from_pyproject(pyproject_path)

    def to_tuple(val, default: tuple[str, ...]) -> tuple[str, ...]:
        if val is None:
            return default
        if isinstance(val, (list, tuple)):
            return tuple(val)
        return default

    _cached_config = Config(
        rst_codeblocks=to_tuple(
            raw.get("rst_codeblocks"), DEFAULT_RST_CODEBLOCKS
        ),
        rst_user_codeblocks=to_tuple(raw.get("rst_user_codeblocks"), ()),
        md_codeblocks=to_tuple(raw.get("md_codeblocks"), DEFAULT_MD_CODEBLOCKS),
        md_user_codeblocks=to_tuple(raw.get("md_user_codeblocks"), ()),
        rst_extensions=to_tuple(
            raw.get("rst_extensions"), DEFAULT_RST_EXTENSIONS
        ),
        rst_user_extensions=to_tuple(raw.get("rst_user_extensions"), ()),
        md_extensions=to_tuple(raw.get("md_extensions"), DEFAULT_MD_EXTENSIONS),
        md_user_extensions=to_tuple(raw.get("md_user_extensions"), ()),
    )
    return _cached_config
