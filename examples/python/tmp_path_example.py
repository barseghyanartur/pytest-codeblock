d = tmp_path / "sub"  # noqa
d.mkdir()  # Create the directory
assert d.is_dir()  # Verify it was created and is a directory
