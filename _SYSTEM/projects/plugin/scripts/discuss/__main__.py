"""Entry point for `python3 scripts/discuss <cmd>` and `python3 -m discuss <cmd>`."""

import sys
from pathlib import Path

if __package__ in (None, ""):
    # Invoked as a directory path: make the package importable, then import absolutely.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from discuss.cli import main
else:
    from .cli import main

main()
