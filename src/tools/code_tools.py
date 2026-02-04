import subprocess
from pathlib import Path

from langchain_core.tools import tool

BLOCKED = ["rm -rf", "rm -fr", "sudo ", "> /dev", "mkfs", "dd if=", ":(){", "chmod 777"]


@tool
def run_command(command: str) -> str:
    """Run a shell command. Blocked: rm -rf, sudo, mkfs, dd, chmod 777."""
    cmd = command.strip()
    if any(b in cmd for b in BLOCKED):
        return "Error: Command not allowed"
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30, cwd="."
        )
        out = result.stdout or result.stderr or ""
        return out.strip() or f"Exit code: {result.returncode}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error: {e}"


@tool
def read_file(file_path: str) -> str:
    """Read file contents. Path relative to workspace root."""
    try:
        return Path(file_path).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error: {e}"


@tool
def write_file(file_path: str, content: str) -> str:
    """Write or overwrite a file."""
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        Path(file_path).write_text(content, encoding="utf-8")
        return f"Wrote {file_path}"
    except Exception as e:
        return f"Error: {e}"


@tool
def list_directory(path: str = ".") -> str:
    """List files and folders in a directory."""
    try:
        items = sorted(Path(path).iterdir(), key=lambda p: (p.is_file(), p.name))
        return "\n".join(f"{'[dir] ' if p.is_dir() else ''}{p.name}" for p in items)
    except Exception as e:
        return f"Error: {e}"


@tool
def search_in_files(pattern: str, path: str = ".") -> str:
    """Search for text pattern in files. Returns matching lines with file paths."""
    results = []
    try:
        for p in Path(path).rglob("*"):
            if p.is_file() and not any(x in str(p) for x in [".git", "__pycache__", "venv", "node_modules"]):
                try:
                    for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                        if pattern.lower() in line.lower():
                            results.append(f"{p}:{i}: {line.strip()}")
                except (OSError, UnicodeDecodeError):
                    pass
        return "\n".join(results[:50]) if results else "No matches"
    except Exception as e:
        return f"Error: {e}"


def get_tools():
    return [read_file, write_file, list_directory, search_in_files, run_command]
