# /// script
# requires-python = ">=3.10"
# ///
"""Render docs/benchmarks/results/*.json into docs/benchmarks/RESULTS.md.

    uv run eval/report.py

Pure formatting: every number comes from a bench.py result file, which in
turn comes from commands recorded in that script. Nothing is computed here
that cannot be recomputed from the committed JSONs.
"""
import datetime, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES = ROOT / "docs" / "benchmarks" / "results"
ORDER = ["tds", "datasheets", "papers", "arxiv", "pmc", "bills",
         "olmocr_multi_column", "olmocr_headers_footers", "olmocr_arxiv_math",
         "olmocr_tables", "olmocr_long_tiny_text", "olmocr_scans"]
REASONS = ["standalone_raster", "no_text_layer", "curves", "diagonals",
           "dense_grid", "stroke_grid"]


def pct(vals, q):
    if not vals:
        return 0.0
    vals = sorted(vals)
    return vals[min(len(vals) - 1, round(q * (len(vals) - 1)))]


def load():
    ds = {}
    for p in sorted(RES.glob("*.json")):
        if p.stem.startswith("_"):
            continue
        ds[p.stem] = json.loads(p.read_text())
    return dict(sorted(ds.items(),
                       key=lambda kv: (ORDER.index(kv[0]) if kv[0] in ORDER
                                       else 99, kv[0])))


def main():
    ds = load()
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                cwd=ROOT, capture_output=True,
                                text=True).stdout.strip()
    except Exception:
        commit = "unknown"
    L = []
    A = L.append
    A("# Benchmark results\n")
    A(f"Generated {datetime.date.today().isoformat()} at commit `{commit}` by "
      "`uv run eval/report.py` from the per-dataset JSONs in "
      "`docs/benchmarks/results/`.")
    A("Reproduce any dataset with `uv run eval/fetch.py <dataset>` then "
      "`uv run eval/bench.py corpus/<dataset>`; inputs are pinned by sha256 "
      "in `eval/manifests/<dataset>.json`.")
    A("Token model: image `(w*h)/750` after fitting inside 1568 px; text "
      "`chars/3.5`; optical baseline renders every page at 140 dpi. Wall "
      "time is the deterministic local pipeline only — model inference is "
      "excluded.\n")

    # ---- table 1: cost -----------------------------------------------------
    A("## Cost: three ways to read each corpus\n")
    A("| dataset | files | pages | MB | full optical | text only | "
      "**pdf-extract** | vs optical | vision calls | local s |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for name, d in ds.items():
        s = d["summary"]
        save = 1 - s["ours_tok"] / s["opt_tok"] if s["opt_tok"] else 0
        A(f"| {name} | {s['files']} | {s['pages']:,} | "
          f"{s['bytes']/1e6:.0f} | {s['opt_tok']:,} | {s['txt_tok']:,} | "
          f"**{s['ours_tok']:,}** | −{save:.0%} | {s['calls']:,} | "
          f"{s['t_ours']:.0f} |")
    A("")
    A("`text only` is always cheapest and always misses every figure, scan "
      "and unparsed table; it is a floor, not an option. `vs optical` is "
      "pdf-extract's token saving against rendering every page.\n")

    # ---- table 2: reasons --------------------------------------------------
    A("## What routing fired, by class\n")
    A("| dataset | " + " | ".join(REASONS) + " | total |")
    A("|---|" + "---|" * (len(REASONS) + 1))
    for name, d in ds.items():
        r = d["summary"].get("reasons", {})
        A(f"| {name} | " + " | ".join(str(r.get(k, 0)) for k in REASONS)
          + f" | {sum(r.values())} |")
    A("")

    # ---- table 3: distribution --------------------------------------------
    A("## Calls-per-page distribution (per file)\n")
    A("| dataset | mean | median | p90 | p99 | max | zero-call files | "
      "over guard (15) | calls>pages |")
    A("|---|---|---|---|---|---|---|---|---|")
    for name, d in ds.items():
        rows = d["rows"]
        cpp = [r["calls"] / r["pages"] for r in rows]
        zero = sum(1 for r in rows if r["calls"] == 0)
        A(f"| {name} | {sum(cpp)/len(cpp):.2f} | {pct(cpp,.5):.2f} | "
          f"{pct(cpp,.9):.2f} | {pct(cpp,.99):.2f} | {max(cpp):.2f} | "
          f"{zero}/{len(rows)} | "
          f"{sum(1 for r in rows if r['over_scale_guard'])} | "
          f"{sum(1 for r in rows if r['calls'] > r['pages'])} |")
    A("")

    # ---- outliers ----------------------------------------------------------
    A("## Outliers, named\n")
    for name, d in ds.items():
        rows = d["rows"]
        over = sorted((r for r in rows if r["calls"] > r["pages"]),
                      key=lambda r: r["calls"] / r["pages"], reverse=True)
        zero_big = [r for r in rows if r["calls"] == 0 and r["big_rasters"] > 0]
        costlier = [r for r in rows if r["ours_tok"] > r["opt_tok"]]
        top = sorted(rows, key=lambda r: r["calls"], reverse=True)[:5]
        A(f"### {name}\n")
        if over:
            A(f"**calls > pages** ({len(over)} files):")
            for r in over[:10]:
                why = max(r["reasons"], key=r["reasons"].get)
                A(f"- `{r['name']}` — {r['calls']} calls / {r['pages']} pages"
                  f" (mostly `{why}`)")
            if len(over) > 10:
                A(f"- … and {len(over) - 10} more")
        if zero_big:
            A(f"\n**zero calls despite ≥1 raster ≥300×300 px** "
              f"({len(zero_big)} files): "
              + ", ".join(f"`{r['name']}`" for r in zero_big[:10])
              + (" …" if len(zero_big) > 10 else ""))
        if costlier:
            A(f"\n**pdf-extract costs MORE than full optical** "
              f"({len(costlier)} files): "
              + ", ".join(f"`{r['name']}` (+{r['ours_tok']-r['opt_tok']:,})"
                          for r in costlier[:10])
              + (" …" if len(costlier) > 10 else ""))
        A("\n**most vision calls:** "
          + ", ".join(f"`{r['name']}` ({r['calls']}/{r['pages']}p)"
                      for r in top) + "\n")
        if d["skips"]:
            A(f"**skipped** ({len(d['skips'])}): "
              + ", ".join(f"`{s['name']}` ({s['skip']})"
                          for s in d["skips"][:10])
              + (" …" if len(d["skips"]) > 10 else "") + "\n")

    # ---- honesty section ---------------------------------------------------
    A("## What this does not measure\n")
    A("- **Figure-description accuracy on text-bearing PDFs.** No public "
      "benchmark scores it; the only accuracy measurement in this repo "
      "remains `eval/oldscans.md` (scanned pages, olmOCR ground truth).")
    A("- **Vector-figure false negatives.** The zero-call cross-check above "
      "uses embedded rasters ≥300×300 px as an independent figure detector; "
      "a chart drawn purely with vector strokes has no such witness, so a "
      "text page whose vector chart was missed is invisible to this suite.")
    A("- **Extraction quality on the new corpora.** No ground truth exists "
      "for arbitrary arXiv/PMC/bill text; quality claims stay pinned to "
      "opendataloader-bench and the byte-identity gate (`eval/gate.py`).")
    A("- **Threshold sensitivity.** Deliberately out of scope: tuning on the "
      "measurement set would invalidate it.\n")

    dest = ROOT / "docs" / "benchmarks" / "RESULTS.md"
    dest.write_text("\n".join(L))
    print(f"wrote {dest.relative_to(ROOT)} ({len(ds)} datasets)")


if __name__ == "__main__":
    main()
