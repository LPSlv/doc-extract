"""Content-addressed cache with atomic publication.

The key is the PDF's bytes *plus* the engine version and the skill's schema
version. Hashing bytes alone would serve artifacts produced by older thresholds
forever, while the README advertises numbers from the current ones.

Publication builds into a staging directory and renames it into place, so a
concurrent reader sees either nothing or a complete artifact -- never a
half-written one, which matters because the vision pass can take minutes.
"""
import hashlib, os, shutil, tempfile
from pathlib import Path

SCHEMA = 1
ENGINE = "pdf-inspector==0.2.6"
DEFAULT_ROOT = Path.home() / ".cache" / "pdf-inspect"


def sha256_file(path, _chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(_chunk), b""):
            h.update(block)
    return h.hexdigest()


def cache_dir(pdf_path, root=None, engine=ENGINE, schema=SCHEMA):
    """Where this PDF's artifact lives, under this engine and schema."""
    root = Path(root) if root is not None else DEFAULT_ROOT
    digest = sha256_file(pdf_path)
    tag = hashlib.sha256(f"{engine}|{schema}".encode()).hexdigest()[:8]
    return root / f"{digest}-{tag}"


def publish(dest, build):
    """Run `build(staging)`, then move the result to `dest` atomically.

    If build raises, the staging directory is removed and `dest` is never
    created. Returns dest.
    """
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(dir=dest.parent, prefix=".staging-"))
    try:
        build(staging)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    try:
        os.rename(staging, dest)
    except OSError:
        # Another agent published first while we were building; theirs is as
        # good as ours, so discard our copy rather than clobber it.
        shutil.rmtree(staging, ignore_errors=True)
    return dest
