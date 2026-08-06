# /// script
# requires-python = ">=3.10"
# dependencies = ["firecrawl-anydoc==0.1.6"]
# ///
"""Cost benchmark for the Office path. Separate from bench.py, deliberately.

bench.py's headline column divides by the cost of rendering every page at 140
dpi. Office documents have no render -- there is no layout engine here -- so
that denominator does not exist, and putting an Office row in the same table
would mean two different baselines silently sharing a column. This measures
what can honestly be measured instead:

  assets found      every image the package actually contains
  sent to vision    what survives the furniture filters and dedup
  charts recovered  spreadsheet chart tables read from the chart definition,
                    which cost no vision call at all
  residue           charts that could not be read, and media that cannot be
                    viewed without a rasterizer -- counted, never hidden

The baseline for "what the filters save" is describing every extracted asset,
which is what a tool that just pulls the images out would hand you.

    uv run eval/office_bench.py corpus/office [--limit K] [--name N]

Writes docs/benchmarks/results/<name>.json.
"""
import collections
import datetime
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))

from filters import _tok                                    # noqa: E402
from office import harvest_office                           # noqa: E402

EXTS = (".docx", ".xlsx", ".pptx")


def bench_file(path):
    row = {"name": path.name, "bytes": path.stat().st_size,
           "ext": path.suffix.lower().lstrip(".")}
    t0 = time.perf_counter()
    try:
        h = harvest_office(str(path))
    except Exception as e:
        row.update(status="crash", detail=f"{type(e).__name__}: {e}")
        return row
    row["t"] = time.perf_counter() - t0
    if h["status"] != "ok":
        row.update(status=h["status"], error=h.get("error"))
        return row

    rasters = [i for i in h["items"] if i["kind"] == "raster"]
    charts = [i for i in h["items"] if i["kind"] == "native_chart"]
    drops = collections.Counter(d["why"].split("(")[0] for d in h["dropped"])

    # Every asset the package held, whether it survived or not. Drops carry px
    # where a dimension was read; those that do not (unviewable media) are
    # counted but cannot be priced, so they are excluded from the baseline
    # rather than guessed at.
    priced_drops = [d for d in h["dropped"] if d.get("px") and all(d["px"])]
    ours = sum(_tok(*i["px"]) for i in rasters if all(i["px"]))
    unfiltered = ours + sum(_tok(*d["px"]) for d in priced_drops)

    row.update(
        status="ok", units=h["pages"], text_chars=h["text_chars"],
        text_tok=int(h["text_chars"] / 3.5),
        assets_found=len(rasters) + len(priced_drops),
        sent_to_vision=len(rasters),
        charts_ok=len(charts),
        charts_unread=drops.get("native_chart_unread", 0),
        unviewable=drops.get("unviewable_media", 0),
        ours_tok=ours, unfiltered_tok=unfiltered,
        drops=dict(drops),
    )
    return row


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    flags = {a.split("=")[0]: a.split("=")[-1] for a in argv if a.startswith("--")}
    if not args:
        print(__doc__, file=sys.stderr)
        return 2
    root = pathlib.Path(args[0])
    files = sorted(p for p in root.rglob("*") if p.suffix.lower() in EXTS)
    if "--limit" in flags:
        files = files[:int(flags["--limit"])]
    name = flags.get("--name", root.name)

    rows = []
    for n, p in enumerate(files, 1):
        rows.append(bench_file(p))
        if n % 20 == 0:
            print(f"  {n}/{len(files)}", file=sys.stderr)

    ok = [r for r in rows if r.get("status") == "ok"]
    by_ext = collections.defaultdict(list)
    for r in ok:
        by_ext[r["ext"]].append(r)

    def agg(rs):
        units = sum(r["units"] for r in rs)
        return {
            "files": len(rs), "units": units,
            "assets_found": sum(r["assets_found"] for r in rs),
            "sent_to_vision": sum(r["sent_to_vision"] for r in rs),
            "calls_per_unit": round(sum(r["sent_to_vision"] for r in rs) / max(1, units), 3),
            "charts_ok": sum(r["charts_ok"] for r in rs),
            "charts_unread": sum(r["charts_unread"] for r in rs),
            "unviewable": sum(r["unviewable"] for r in rs),
            "text_tok": sum(r["text_tok"] for r in rs),
            "ours_tok": sum(r["ours_tok"] for r in rs),
            "unfiltered_tok": sum(r["unfiltered_tok"] for r in rs),
            "t": round(sum(r.get("t", 0) for r in rs), 1),
        }

    summary = {"all": agg(ok), **{e: agg(rs) for e, rs in sorted(by_ext.items())}}
    failures = collections.Counter(r.get("error") or r.get("status")
                                   for r in rows if r.get("status") != "ok")
    out = {
        "dataset": name, "kind": "office",
        "generated": datetime.datetime.now(datetime.timezone.utc)
                             .replace(microsecond=0).isoformat(),
        "engine": "anydoc==0.1.6",
        "baseline": "describe every extracted asset, before furniture filters and dedup",
        "files_total": len(rows), "files_ok": len(ok),
        "failures": dict(failures),
        "summary": summary, "rows": rows,
    }
    dest = ROOT / "docs" / "benchmarks" / "results" / f"{name}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=1))

    a = summary["all"]
    print(f"\n{name}: {len(ok)}/{len(rows)} converted, {a['units']} units")
    print(f"  assets found {a['assets_found']} -> {a['sent_to_vision']} sent to vision "
          f"({a['calls_per_unit']} per unit)")
    print(f"  charts recovered {a['charts_ok']} at zero vision cost, "
          f"{a['charts_unread']} unreadable")
    print(f"  unviewable media {a['unviewable']}")
    print(f"  tokens: text {a['text_tok']:,} + vision {a['ours_tok']:,} "
          f"vs {a['unfiltered_tok']:,} unfiltered")
    if failures:
        print(f"  failures: {dict(failures)}")
    print(f"  -> {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
