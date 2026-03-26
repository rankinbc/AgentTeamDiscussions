"""Atomic file I/O utility."""

import os
from pathlib import Path


def write_atomic(path: Path | str, content: str, encoding: str = "utf-8") -> None:
    """Write content to path atomically: write to .tmp, then os.replace().

    Args:
        path: Destination file path. Parent directory must already exist.
        content: Text content to write.
        encoding: File encoding (default: utf-8).

    Raises:
        FileNotFoundError: If the parent directory does not exist.
        OSError: On other I/O failures.
    """
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding=encoding)
    os.replace(tmp, path)
