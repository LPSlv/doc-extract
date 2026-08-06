"""Tests for cache keying and atomic publication.

Two failure modes these guard against: serving a stale artifact after the engine
or thresholds change (§4 Phase 0), and a second agent observing a half-written
cache directory (§11).
"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skills" / "doc-extract"))

import pytest
from cache import cache_dir, publish, SCHEMA


def test_same_bytes_at_different_paths_share_a_cache_dir(tmp_path):
    a = tmp_path / "a.pdf"; a.write_bytes(b"%PDF-1.4 hello")
    b = tmp_path / "deep" / "b.pdf"; b.parent.mkdir(); b.write_bytes(b"%PDF-1.4 hello")
    assert cache_dir(a, root=tmp_path / "c") == cache_dir(b, root=tmp_path / "c")


def test_different_bytes_get_different_cache_dirs(tmp_path):
    a = tmp_path / "a.pdf"; a.write_bytes(b"%PDF-1.4 one")
    b = tmp_path / "b.pdf"; b.write_bytes(b"%PDF-1.4 two")
    assert cache_dir(a, root=tmp_path / "c") != cache_dir(b, root=tmp_path / "c")


def test_engine_version_change_invalidates_the_cache(tmp_path):
    a = tmp_path / "a.pdf"; a.write_bytes(b"%PDF-1.4 hello")
    old = cache_dir(a, root=tmp_path / "c", engine="pdf-inspector==0.2.6")
    new = cache_dir(a, root=tmp_path / "c", engine="pdf-inspector==0.3.0")
    assert old != new, "upgrading the engine must not serve stale artifacts"


def test_schema_version_change_invalidates_the_cache(tmp_path):
    a = tmp_path / "a.pdf"; a.write_bytes(b"%PDF-1.4 hello")
    old = cache_dir(a, root=tmp_path / "c", schema=SCHEMA)
    new = cache_dir(a, root=tmp_path / "c", schema=SCHEMA + 1)
    assert old != new, "changing thresholds must not serve stale artifacts"


def test_publish_is_atomic_so_a_partial_write_is_never_visible(tmp_path):
    dest = tmp_path / "c" / "abc"

    def build(staging):
        (staging / "doc.md").write_text("hello")
        raise RuntimeError("vision pass died halfway")

    with pytest.raises(RuntimeError):
        publish(dest, build)
    assert not dest.exists(), "a failed run must leave no cache directory behind"


def test_publish_makes_the_directory_visible_on_success(tmp_path):
    dest = tmp_path / "c" / "abc"

    def build(staging):
        (staging / "doc.md").write_text("hello")
        (staging / "manifest.json").write_text(json.dumps({"items": []}))

    publish(dest, build)
    assert (dest / "doc.md").read_text() == "hello"
