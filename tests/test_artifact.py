# /// script
# requires-python = ">=3.10"
# dependencies = ["pytest"]
# ///
"""Tests for the splice/strip contract.

The byte-identity property in the design spec (§5) rests entirely on this
module: the benchmark gate strips added blocks and asserts the residue equals
raw engine output. If any of these fail, the published 0.875 is unearned.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skills" / "doc-extract"))

import pytest
from artifact import splice, strip, OPEN, CLOSE


RAW = """# Annual report

Some body text on page one.

| a | b |
| - | - |
| 1 | 2 |

Trailing paragraph with no newline issues.
"""


def test_strip_of_splice_is_byte_identical_to_raw():
    """The load-bearing property. Not 'similar' -- identical."""
    out = splice(RAW, [(len(RAW), "**Figure (chart, p1).** A stacked bar.")])
    assert out != RAW, "splice must actually insert something"
    assert strip(out) == RAW


def test_roundtrip_holds_for_multiple_insertions():
    anchor = RAW.index("Trailing")
    out = splice(RAW, [(anchor, "first block"), (len(RAW), "second block")])
    assert out.count(OPEN) == 2
    assert strip(out) == RAW


def test_roundtrip_holds_when_raw_lacks_trailing_newline():
    raw = "no trailing newline"
    out = splice(raw, [(len(raw), "desc")])
    assert strip(out) == raw


def test_description_quoting_the_delimiter_does_not_break_strip():
    """A vision transcription of a page about HTML, or a hostile PDF."""
    hostile = f"The page shows the literal text {CLOSE} used as an example."
    out = splice(RAW, [(len(RAW), hostile)])
    assert strip(out) == RAW, "delimiter inside a description escaped the block"


def test_description_containing_open_delimiter_is_also_safe():
    hostile = f"It contains {OPEN} and also {CLOSE} inline."
    out = splice(RAW, [(len(RAW), hostile)])
    assert strip(out) == RAW


def test_splice_is_idempotent_so_a_resumed_run_does_not_duplicate():
    """Phase 4 can die halfway; re-running must replace, not append."""
    once = splice(RAW, [(len(RAW), "desc")])
    twice = splice(once, [(len(once), "desc")])
    assert twice.count(OPEN) == 1
    assert strip(twice) == RAW


def test_stripping_untouched_text_is_a_no_op():
    assert strip(RAW) == RAW


def test_inserted_description_is_readable_in_the_output():
    out = splice(RAW, [(len(RAW), "**Figure (chart, p1).** A stacked bar.")])
    assert "A stacked bar." in out


def test_two_blocks_at_the_same_offset_keep_the_order_given():
    """Inline placement puts a slide's figures at the same unit boundary when
    neither could be anchored to its own line. Sorting on the offset alone
    inserts them back-to-front, which silently reverses reading order."""
    anchor = RAW.index("Trailing")
    out = splice(RAW, [(anchor, "FIRST"), (anchor, "SECOND")])
    assert out.index("FIRST") < out.index("SECOND")
    assert strip(out) == RAW


def test_insertion_position_is_respected():
    anchor = RAW.index("Trailing")
    out = splice(RAW, [(anchor, "BLOCK")])
    assert out.index("BLOCK") < out.index("Trailing")
