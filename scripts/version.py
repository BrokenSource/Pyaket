"""
Updates version strings in relevant files

Usage:
    python version.py 1.0.0
"""
import re
import sys
from pathlib import Path

REPO: Path = Path(__file__).parent.parent
"""Path to the repository root"""

if __name__ == "__main__":
    version: str = sys.argv[1]

    # Only for relevant files
    for path in tuple((
        (REPO/"pyproject.toml"),
        (REPO/"pyaket"/"__init__.py"),
        (REPO/"pyaket"/"Cargo.toml"),
    )):
        path.write_text(re.sub(
            r'^(__version__|version)(.*?=\s*)"[^"]*"',
            fr'\1\2"{version}"', # For real, man
            path.read_text("utf-8"),
            flags=re.MULTILINE
        ))
