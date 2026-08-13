# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Render `whole_document` and `curves` firings for labelling.

`docs/NEXT.md` item 2: in the 30-page figure-QA v3 sample, 11 routed pages
carried no figure at all, concentrated in `whole_document` (4 of 9) and
`curves` (4 of 11). Thirty observations cannot condemn two branches -
`stroke_grid` was 3-for-3 wrong in a THREE-observation sample and turned out
to be 42% waste, not 100%, when labelled exhaustively. So a small sample is
untrustworthy in both directions and this builds the durable artifact instead.

Two things the figure-QA sample was, and this is not:

  - it sampled only pages carrying >=400 characters of extractable text
    (`figqa_select.py:MIN_PAGE_CHARS`), which biases hard towards prose and
    away from full-page figures. This enumerates every firing.
  - it sampled one page per document and one document per draw, so a 96-page
    `whole_document` collapse counted once and a lone `curves` page counted
    once. This counts pages.

Same 711-document base as `eval/strokegrid.md` - datasheets, pmc, arxiv,
papers, tds - so the two artifacts are comparable.

    uv run eval/nofigure_render.py                 # harvest, sample, render
    uv run eval/nofigure_render.py --reuse         # skip the harvest
    uv run eval/nofigure_render.py --shard i/n     # internal: one serial shard

Harvesting is fanned out as `--shard` SUBPROCESSES running `harvest()` in a
plain loop, not through `harvest._harvest_all`. That function's
ProcessPoolExecutor deadlocked on this corpus - every worker parked in
futex_do_wait with the parent blocked on the result queue, no exception, no
progress - and its `except` cannot catch a hang. Separate OS processes each
running the serial path have no shared pool to deadlock on.

The facts carried alongside each render are the ones a labeller should not
have to judge by eye:

  page_chars     extractable text on the page
  n_images       rasters placed on the page
  n_drawings     vector paths on the page (0 with n_images 0: nothing to see)
  md_chars       markdown the extractor already produced for this page
  has_md_table   that markdown already contains a pipe table
  has_caption    "Fig(ure) N" / "Table N" / "Chart N" occurs in the page text
"""
import collections
import json
import pathlib
import random
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
import fitz                                                   # noqa: E402
import pdf_inspector as pi                                    # noqa: E402
from harvest import (batch_furniture, drop_batch_furniture,   # noqa: E402
                     harvest, page_geometry)

OUT = ROOT / "eval" / "nofigure"
PARTS = OUT / "parts"
CORPORA = ["datasheets", "pmc", "arxiv", "papers", "tds"]
BRANCHES = ("whole_document", "curves")
DPI = 130
SHARDS = 6

# Labelling budget. Above this the population is sampled, never truncated.
# The seed is fixed and was not reshuffled until the draw said something
# convenient; the strata report below prints exactly what went unlabelled.
SAMPLE_MAX = 240
SEED = 20260813

CAPTION = re.compile(r"\b(Fig(?:ure)?\.?|Table|Chart|Scheme|Plate)\s*\.?\s*\d",
                     re.I)


def corpus_paths():
    """(corpus, path) for all 711 documents, in a stable order."""
    out = []
    for c in CORPORA:
        out += [(c, p) for p in sorted((ROOT / "corpus" / c).glob("*.pdf"))]
    return out


# ------------------------------------------------------------------- harvest
def run_shard(i, n):
    """Harvest every n-th document serially and write a part file."""
    PARTS.mkdir(parents=True, exist_ok=True)
    recs = []
    todo = corpus_paths()[i::n]
    for k, (c, p) in enumerate(todo):
        try:
            r = harvest(str(p))
        except Exception as e:
            r = {"status": "error", "error": f"{type(e).__name__}: {e}",
                 "path": str(p)}
        recs.append({"corpus": c, "path": r.get("path", str(p)),
                     "name": p.name, "status": r.get("status"),
                     "pages": r.get("pages", 0),
                     "items": r.get("items") or [],
                     "dropped": r.get("dropped") or [],
                     "page_sigs": r.get("page_sigs") or {}})
        if (k + 1) % 20 == 0:
            print(f"shard {i}: {k + 1}/{len(todo)}", file=sys.stderr, flush=True)
    (PARTS / f"shard{i}.json").write_text(json.dumps(recs))
    print(f"shard {i}: done {len(recs)}", file=sys.stderr, flush=True)


def harvest_all():
    PARTS.mkdir(parents=True, exist_ok=True)
    for f in PARTS.glob("shard*.json"):
        f.unlink()
    procs = [subprocess.Popen(
        [sys.executable, str(pathlib.Path(__file__).resolve()),
         "--shard", f"{i}/{SHARDS}"]) for i in range(SHARDS)]
    bad = [i for i, p in enumerate(procs) if p.wait() != 0]
    if bad:
        raise SystemExit(f"shards failed: {bad}")
    recs = []
    for i in range(SHARDS):
        recs += json.loads((PARTS / f"shard{i}.json").read_text())
    return recs


def collect(recs):
    """Apply cross-document furniture per corpus, then pull the two branches.

    Batched per corpus, exactly as `strokegrid_validate.py` batches, because
    `batch_furniture` is defined at batch scope: a signature must recur across
    >50% of the batch's DOCUMENTS, so pooling five corpora into one batch
    would silently disable it.
    """
    firings, meta, sanity = [], [], collections.Counter()
    for c in CORPORA:
        rs = [r for r in recs if r["corpus"] == c]
        drop_batch_furniture(rs, batch_furniture(rs))
        ok = [r for r in rs if r["status"] == "ok"]
        for r in ok:
            collapsed = any(d.get("why") == "cost_guard" for d in r["dropped"])
            for it in r["items"]:
                sanity[it["reason"]] += 1
                if it["reason"] not in BRANCHES:
                    continue
                firings.append({
                    "corpus": c,
                    "doc": str(pathlib.Path(r["path"]).relative_to(ROOT)),
                    "name": r["name"], "page": it["page"], "id": it["id"],
                    "reason": it["reason"], "npages": r["pages"],
                    "collapsed": collapsed, "doc_calls": len(r["items"])})
        meta.append({"corpus": c, "documents": len(rs), "ok": len(ok),
                     "errors": len(rs) - len(ok),
                     "vision_calls": sum(len(r["items"]) for r in ok)})
    return firings, meta, sanity


# --------------------------------------------------------------------- sample
def stratified(firings, cap=SAMPLE_MAX, seed=SEED):
    """Sample within each (branch, corpus) cell. Returns (sample, report).

    Two departures from a flat proportional draw, both stated rather than
    buried:

    - the budget is split EQUALLY between the two branches (or as close as
      each population allows). They are separate routing decisions with
      separate answers, and a flat draw would give `curves` almost nothing,
      because one collapsed 96-page paper contributes 96 `whole_document`
      firings and a `curves` page contributes one. The consequence is that
      the pooled rate is NOT the population rate; every pooled figure in the
      write-up has to be reweighted by the population shares in firings.json.
    - within a branch the draw IS proportional by corpus, with a floor of one
      per non-empty cell so no corpus is silently erased.

    Nothing is truncated silently: the report names every cell and how many
    of it go unlabelled.
    """
    if len(firings) <= cap:
        return list(firings), []
    cells = collections.defaultdict(list)
    for f in firings:
        cells[(f["reason"], f["corpus"])].append(f)
    per_branch = {b: [k for k in cells if k[0] == b] for b in BRANCHES}
    per_branch = {b: ks for b, ks in per_branch.items() if ks}

    budget = {}
    share = cap // len(per_branch)
    left = cap
    for j, (b, ks) in enumerate(sorted(per_branch.items())):
        pop = sum(len(cells[k]) for k in ks)
        want = min(share if j < len(per_branch) - 1 else left, pop)
        budget[b] = want
        left -= want
    # any budget a small branch could not absorb goes to the others
    for b in sorted(budget):
        pop = sum(len(cells[k]) for k in per_branch[b])
        if left > 0 and budget[b] < pop:
            add = min(left, pop - budget[b])
            budget[b] += add
            left -= add

    take = {}
    for b, ks in per_branch.items():
        pop = sum(len(cells[k]) for k in ks)
        exact = {k: len(cells[k]) * budget[b] / pop for k in ks}
        t = {k: min(len(cells[k]), max(1, int(exact[k]))) for k in ks}
        while sum(t.values()) > budget[b]:
            k = max((k for k in ks if t[k] > 1), key=lambda k: t[k])
            t[k] -= 1
        for k in sorted(ks, key=lambda k: exact[k] - int(exact[k]), reverse=True):
            if sum(t.values()) >= budget[b]:
                break
            if t[k] < len(cells[k]):
                t[k] += 1
        take.update(t)

    rng = random.Random(seed)
    sample, report = [], []
    for k in sorted(cells):
        pool = sorted(cells[k], key=lambda f: (f["doc"], f["page"]))
        n = min(take.get(k, 0), len(pool))
        sample += rng.sample(pool, n)
        report.append({"branch": k[0], "corpus": k[1], "population": len(pool),
                       "sampled": n, "not_labelled": len(pool) - n})
    sample.sort(key=lambda f: (f["reason"], f["corpus"], f["doc"], f["page"]))
    return sample, report


# --------------------------------------------------------------------- render
def render(sample):
    rows, md_cache = [], {}
    for i, f in enumerate(sample):
        doc = str(ROOT / f["doc"])
        if doc not in md_cache:
            try:
                md_cache[doc] = pi.extract_pages_markdown(doc).pages
            except Exception:
                md_cache[doc] = []
        # pdf_inspector's PageMarkdown.page is 0-BASED while harvest's item
        # pages are 1-based. Matching them directly reads the FOLLOWING page;
        # that exact bug produced a wrong number in an earlier strokegrid pass.
        md = next((p.markdown for p in md_cache[doc]
                   if p.page == f["page"] - 1), "") or ""
        tag = f"n{i + 1:03d}"
        try:
            with fitz.open(doc) as d:
                pg = d[f["page"] - 1]
                pg.get_pixmap(dpi=DPI).save(str(OUT / "pages" / f"{tag}.png"))
                text = pg.get_text()
                g = page_geometry(pg)
                n_images = len(pg.get_images(full=True))
                n_drawings = len(pg.get_cdrawings())
        except Exception as e:
            print(f"  SKIP {tag} {f['name']} p{f['page']}: {e}", file=sys.stderr)
            continue
        rows.append({
            "tag": tag, "corpus": f["corpus"], "file": f["name"],
            "page": f["page"], "npages": f["npages"], "branch": f["reason"],
            "collapsed": f["collapsed"], "doc_calls": f["doc_calls"],
            "page_chars": len(text.strip()), "n_images": n_images,
            "n_drawings": n_drawings, "md_chars": len(md.strip()),
            "has_md_table": "|---" in md or "| ---" in md,
            "has_caption": bool(CAPTION.search(text)),
            "curves": g["curves"], "diagonals": g["diagonals"],
            "axis_h": g["axis_h"], "axis_v": g["axis_v"], "rects": g["rects"],
            "stroke_frac": g["stroke_frac"], "stroke_aspect": g["stroke_aspect"],
            "ink": g["ink"], "vx_pos": len(g["vx_pos"])})
        if (i + 1) % 50 == 0:
            print(f"  rendered {i + 1}/{len(sample)}", file=sys.stderr)
    return rows


def main(reuse=False):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pages").mkdir(exist_ok=True)
    fpath = OUT / "firings.json"

    if reuse and fpath.exists():
        blob = json.loads(fpath.read_text())
        firings, meta, sanity = blob["firings"], blob["corpora"], blob["all_branches"]
        print(f"reusing {len(firings)} firings from {fpath}", file=sys.stderr)
    else:
        print(f"harvesting {len(corpus_paths())} documents in {SHARDS} shards…",
              file=sys.stderr)
        firings, meta, sanity = collect(harvest_all())

    by = collections.Counter((f["reason"], f["corpus"]) for f in firings)
    fpath.write_text(json.dumps({
        "corpora": meta, "branches": list(BRANCHES),
        "n_firings": len(firings),
        "n_documents": len({f["doc"] for f in firings}),
        "all_branches": dict(sanity),
        "by_branch_corpus": {f"{b}/{c}": n for (b, c), n in sorted(by.items())},
        "firings": firings}, indent=1))

    sample, report = stratified(firings)
    if report:
        n_drop = sum(r["not_labelled"] for r in report)
        print(f"\npopulation {len(firings)} > cap {SAMPLE_MAX}: drawing "
              f"{len(sample)} with seed {SEED}", file=sys.stderr)
        print(f"NOT LABELLED: {n_drop} firings, by cell:", file=sys.stderr)
        for r in sorted(report, key=lambda r: -r["not_labelled"]):
            print(f"  {r['branch']:<15} {r['corpus']:<11} pop {r['population']:>5}"
                  f"  sampled {r['sampled']:>4}  unlabelled {r['not_labelled']:>5}",
                  file=sys.stderr)

    rows = render(sample)
    (OUT / "index.json").write_text(json.dumps({
        "dpi": DPI, "seed": SEED, "cap": SAMPLE_MAX,
        "population": len(firings), "sampled": len(sample),
        "rendered": len(rows), "strata": report, "rows": rows}, indent=1))

    print(f"\nall branches, all corpora: {dict(sanity)}")
    print(f"population : {len(firings)} firings over "
          f"{len({f['doc'] for f in firings})} documents")
    for (b, c), n in sorted(by.items()):
        print(f"  {b:<15} {c:<11} {n:>5}")
    print(f"rendered   : {len(rows)} -> {OUT / 'pages'}")


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--shard" in argv:
        i, n = argv[argv.index("--shard") + 1].split("/")
        run_shard(int(i), int(n))
    else:
        main(reuse="--reuse" in argv)
