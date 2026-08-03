# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf==1.28.0"]
# ///
"""Pin a corpus: per-file sha256 + page counts + size distribution.

    uv run eval/manifest.py corpus/<dataset> [...]

Writes eval/manifests/<dataset>.json (dataset name = directory basename).
Committed to git so every benchmark result is tied to exact inputs; the
corpora themselves stay gitignored for copyright reasons.
"""
import datetime, hashlib, json, pathlib, statistics, sys
import fitz

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANI = ROOT / "eval" / "manifests"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pct(sorted_vals, q):
    if not sorted_vals:
        return 0
    i = min(len(sorted_vals) - 1, round(q * (len(sorted_vals) - 1)))
    return sorted_vals[int(i)]


def build(folder: pathlib.Path):
    files = []
    for f in sorted(folder.glob("*.pdf")):
        try:
            with fitz.open(str(f)) as d:
                pages = len(d)
        except Exception:
            pages = None                      # recorded, still pinned
        files.append({"name": f.name, "sha256": sha256(f),
                      "bytes": f.stat().st_size, "pages": pages})
    pp = sorted(x["pages"] for x in files if x["pages"] is not None)
    out = {
        "dataset": folder.name,
        "generated": datetime.date.today().isoformat(),
        "summary": {
            "files": len(files),
            "pages": sum(pp),
            "bytes": sum(x["bytes"] for x in files),
            "unreadable": sum(1 for x in files if x["pages"] is None),
            "page_dist": {"min": pp[0] if pp else 0,
                          "p25": pct(pp, .25), "median": pct(pp, .50),
                          "p75": pct(pp, .75), "p95": pct(pp, .95),
                          "max": pp[-1] if pp else 0,
                          "mean": round(statistics.mean(pp), 1) if pp else 0},
        },
        "files": files,
    }
    MANI.mkdir(exist_ok=True)
    dest = MANI / f"{folder.name}.json"
    dest.write_text(json.dumps(out, indent=1) + "\n")
    s = out["summary"]
    print(f"{folder.name}: {s['files']} files, {s['pages']} pages, "
          f"{s['bytes']/1e6:.1f} MB -> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    for a in sys.argv[1:]:
        build(pathlib.Path(a).resolve())
