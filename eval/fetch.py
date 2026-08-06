# /// script
# requires-python = ">=3.10"
# ///
"""Rebuild a benchmark corpus from its pinned URL list.

    uv run eval/fetch.py <dataset> [...]        # e.g. arxiv pmc bills
    uv run eval/fetch.py --verify <dataset>     # also check eval/manifests/<ds>.json

Reads eval/manifests/<dataset>.urls.tsv (filename<TAB>url[<TAB>sha256]) and
downloads into corpus/<dataset>/. Anything that is not a real document of the
kind its name claims (magic bytes, and the content-types part for OOXML) or
fails a pinned sha256 is deleted and reported, never kept.

A URL of the form <zip-url>!<member-path> takes one member out of an archive.
Some corpora are only published as per-type zips -- govdocs1's docx and xlsx
are 163 and 37 documents in two files -- and fetching the archive once beats
200 requests. The archive is cached under corpus/_archives/ and reused.
Idempotent: existing valid files are skipped. arXiv is fetched serially at
one request per 3 s per their robots policy; other hosts get 6 workers.
"""
import concurrent.futures as cf
import hashlib, json, pathlib, sys, threading, time, urllib.request, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANI = ROOT / "eval" / "manifests"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) doc-extract-bench/1.0"}
# Some hosts refuse a generic agent and serve an HTML block page instead of the
# file. SEC's fair-access policy asks for a contact address in the agent, and a
# bare one gets HTML that would otherwise be written to disk as a .xlsx.
HOST_UA = {
    "www.sec.gov": "doc-extract-bench/1.0 (contact: lenards@optonics.eu)",
}
SLOW_HOSTS = {"export.arxiv.org": 3.0, "www.sec.gov": 0.15}   # host -> min seconds between hits
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


ARCHIVES = ROOT / "corpus" / "_archives"
_arch_lock = threading.Lock()


def _archive(url: str):
    """Download an archive once and hand back its path. Thread-safe."""
    ARCHIVES.mkdir(parents=True, exist_ok=True)
    dest = ARCHIVES / urllib.parse.urlparse(url).path.rsplit("/", 1)[-1]
    with _arch_lock:
        if dest.exists() and dest.stat().st_size > 1000:
            return dest
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)
    return dest


def fetch_member(dest: pathlib.Path, url: str, pin: str | None):
    import zipfile
    zip_url, member = url.split("!", 1)
    try:
        arch = _archive(zip_url)
        with zipfile.ZipFile(arch) as z:
            dest.write_bytes(z.read(member))
    except Exception as e:
        dest.unlink(missing_ok=True)
        return f"error {type(e).__name__}"
    if not _valid(dest):
        dest.unlink()
        return "not-a-document"
    if pin and sha256(dest) != pin:
        dest.unlink()
        return "sha256-mismatch"
    return "new"


def fetch_one(dest: pathlib.Path, url: str, pin: str | None):
    if dest.exists() and dest.stat().st_size > 1000:
        return "have"
    if "!" in url:
        return fetch_member(dest, url, pin)
    host = urllib.parse.urlparse(url).netloc
    for attempt in (1, 2):
        polite(host)
        try:
            headers = dict(UA)
            if host in HOST_UA:
                headers["User-Agent"] = HOST_UA[host]
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
            break
        except Exception as e:
            if attempt == 2:
                dest.unlink(missing_ok=True)
                return f"error {type(e).__name__}"
            time.sleep(2)
    if not _valid(dest):
        dest.unlink()
        return "not-a-document"
    if pin and sha256(dest) != pin:
        dest.unlink()
        return "sha256-mismatch"
    return "new"


def _valid(dest: pathlib.Path):
    """A real document of the kind this filename claims, by content.

    Extension-based checks would pass an HTML block page renamed .xlsx, which
    is exactly what a rate-limiting host serves. OOXML packages are zips whose
    content-types part must be present, so the check is cheap and specific.
    """
    if dest.stat().st_size < 1000:
        return False
    head = dest.open("rb").read(4)
    if dest.suffix.lower() == ".pdf":
        return head[:4] == b"%PDF"
    if dest.suffix.lower() in (".docx", ".xlsx", ".pptx"):
        if head != b"PK\x03\x04":
            return False
        try:
            import zipfile
            with zipfile.ZipFile(dest) as z:
                return "[Content_Types].xml" in z.namelist()
        except Exception:
            return False
    return True


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
