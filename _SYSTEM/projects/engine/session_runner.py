"""Backward-compatible wrapper. Code lives in session/runner.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from session.runner import *
from session.runner import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
