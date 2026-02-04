import tempfile
from pathlib import Path

import pytest

from src.tools.code_tools import (
    list_directory,
    read_file,
    run_command,
    search_in_files,
    write_file,
)


def test_read_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("hello world")
        path = f.name
    try:
        assert read_file.invoke({"file_path": path}) == "hello world"
    finally:
        Path(path).unlink()


def test_write_file():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test.txt"
        result = write_file.invoke({"file_path": str(path), "content": "foo"})
        assert "Wrote" in result
        assert path.read_text() == "foo"


def test_list_directory():
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "a.txt").touch()
        (Path(tmp) / "b").mkdir()
        result = list_directory.invoke({"path": tmp})
        assert "a.txt" in result
        assert "b" in result


def test_search_in_files():
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "x.py"
        f.write_text("def foo():\n    pass\n")
        result = search_in_files.invoke({"pattern": "foo", "path": tmp})
        assert "foo" in result


def test_run_command_allowed():
    result = run_command.invoke({"command": "echo hello"})
    assert "hello" in result


def test_run_command_blocked():
    result = run_command.invoke({"command": "rm -rf /"})
    assert "not allowed" in result
