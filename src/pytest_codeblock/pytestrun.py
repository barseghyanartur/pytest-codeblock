"""
Helper module for running pytest-style tests found inside executed code blocks.
When a code block is marked with `pytestrun`, its code is written to a
temporary file and executed by pytest as a subprocess, so that fixtures,
markers, setup/teardown, and assertions all work correctly.
"""
import os
import subprocess
import sys
import tempfile

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("run_pytest_style_code",)


def run_pytest_style_code(
    code: str,
    snippet_name: str,
    path: str,
) -> None:
    """
    Write the code block to a temporary file and run it with pytest.
    Raises AssertionError on any test failures.
    """
    tmpdir = tempfile.mkdtemp(prefix="pytest_codeblock_")
    tmpfile = os.path.join(tmpdir, f"{snippet_name}.py")
    try:
        with open(tmpfile, "w") as f:
            f.write(code)
        project_root = os.getcwd()
        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join(sys.path)
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest", tmpfile,
                f"--rootdir={project_root}",
                "--no-header", "-q",
            ],
            capture_output=True,
            text=True,
            cwd=project_root,
            env=env,
        )
        if result.returncode != 0:
            output = (result.stdout + result.stderr).strip()
            raise AssertionError(
                f"pytestrun block `{snippet_name}` in {path} failed:\n\n"
                f"{output}"
            )
    finally:
        try:
            os.unlink(tmpfile)
            os.rmdir(tmpdir)
        except OSError:
            pass
