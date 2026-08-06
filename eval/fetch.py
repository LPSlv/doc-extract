# /// script
# requires-python = ">=3.10"
# ///
"""Rebuild a benchmark corpus from its pinned URL list.

    uv run eval/fetch.py <dataset> [...]        # e.g. arxiv pmc bills
    uv run eval/fetch.py --verify <dataset>     # also check eval/manifests/<ds>.json

Reads eval/manifests/<dataset>.urls.tsv (filename<TAB>url[<TAB>sha256]) and
downloads into corpus/<dataset>/. Anything that is not a real PDF (magic
bytes) or fails a pinned sha256 is deleted and reported, never kept.
Idempotent: existing valid files are skipped. arXiv is fetched serially at
one request per 3 s per their robots policy; other hosts get 6 workers.
"""
import concurrent.futures as cf
import hashlib, json, pathlib, sys, threading, time, urllib.request, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANI = ROOT / "eval" / "manifests"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) doc-extract-bench/1.0"}
SLOW_HOSTS = {"export.arxiv.org": 3.0}          # host -> min seconds between hits
_locks: dict[str, threading.Lock] = {}
_last: dict[str, float] = {}


def polite(host):
    delay = SLOW_HOSTS.get(host)
    if not delay:
        return
    with _locks.setdefault(host, threading.Lock()):
        wait = _last.get(host, 0) + delay - time.time()
        if wait > 0:
            time.sleep(wait)
        _last[host] = time.time()


def sha256(p: pathlib.Path):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_one(dest: pathlib.Path, url: str, pin: str | None):
    if dest.exists() and dest.stat().st_size > 1000:
        return "have"
    host = urllib.parse.urlparse(url).netloc
    for attempt in (1, 2):
        polite(host)
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
            break
        except Exception as e:
            if attempt == 2:
                dest.unlink(missing_ok=True)
                return f"error {type(e).__name__}"
            time.sleep(2)
    head = dest.open("rb").read(5)
    if head != b"%PDF-" or dest.stat().st_size < 1000:
        dest.unlink()
        return "not-pdf"
    if pin and sha256(dest) != pin:
        dest.unlink()
        return "sha256-mismatch"
    return "new"


def run(dataset: str, verify: bool):
    tsv = MANI / f"{dataset}.urls.tsv"
    if not tsv.exists():
        print(f"{dataset}: no URL list at {tsv}"); return 1
    rows = [l.split("\t") for l in tsv.read_text().splitlines() if l.strip()]
    out = ROOT / "corpus" / dataset
    out.mkdir(parents=True, exist_ok=True)
    stats: dict[str, int] = {}
    failures = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(fetch_one, out / r[0], r[1],
                          r[2] if len(r) > 2 else None): r[0] for r in rows}
        for fut in cf.as_completed(futs):
            res = fut.result()
            stats[res] = stats.get(res, 0) + 1
            if res not in ("have", "new"):
                failures.append((futs[fut], res))
    got = stats.get("have", 0) + stats.get("new", 0)
    print(f"{dataset}: {got}/{len(rows)} present  {stats}")
    for name, why in sorted(failures)[:15]:
        print(f"  miss {name}: {why}")
    if len(failures) > 15:
        print(f"  ... and {len(failures) - 15} more")
    if verify:
        mf = MANI / f"{dataset}.json"
        if not mf.exists():
            print(f"  no manifest to verify against ({mf.name} missing)")
            return 0
        want = {f["name"]: f["sha256"] for f in json.loads(mf.read_text())["files"]}
        bad = [n for n, s in want.items()
               if not (out / n).exists() or sha256(out / n) != s]
        print(f"  manifest: {len(want) - len(bad)}/{len(want)} verified"
              + (f", MISMATCH: {bad[:5]}" if bad else ""))
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--verify"]
    verify = "--verify" in sys.argv
    if not args:
        print(__doc__); sys.exit(2)
    sys.exit(max(run(d, verify) for d in args))
