"""Assert the verbatim block in reference/harvest-block.md matches harvest.py.

The skill promises an agent can paste the block and get identical routing. If
the two drift, that promise is false and the spec's numbers stop being
reproducible from what the agent actually runs.

Usage:  python tests/check_sync.py [--fix]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "skills" / "pdf-extract" / "harvest.py"
DOC = ROOT / "skills" / "pdf-extract" / "reference" / "harvest-block.md"

HEADER = """# harvest-block

Verbatim copy of `harvest.py`, for agents that cannot execute a file. Generated
by `tests/check_sync.py --fix`; do not edit by hand.

```python
"""
FOOTER = "```\n"


def render():
    return HEADER + SRC.read_text() + FOOTER


def main():
    want = render()
    if "--fix" in sys.argv:
        DOC.parent.mkdir(parents=True, exist_ok=True)
        DOC.write_text(want)
        print(f"wrote {DOC.relative_to(ROOT)}")
        return 0
    if not DOC.exists():
        print(f"MISSING: {DOC.relative_to(ROOT)} -- run with --fix")
        return 1
    if DOC.read_text() != want:
        print(f"OUT OF SYNC: {DOC.relative_to(ROOT)} != {SRC.relative_to(ROOT)}")
        print("run: python tests/check_sync.py --fix")
        return 1
    print("in sync")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
