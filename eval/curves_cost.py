# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""What the `vendor_curves` test itself costs, isolated from cache effects.

`eval/curves_validate.py` harvests each document twice, shipped then patched,
and the wall-clock difference between those two runs is NOT the cost of the
rule: the second run reads a warm page cache and can come out FASTER than the
first. Compute cost sank soft-mask suppression (`eval/rejected-signals.md`,
40 ms/document for 0.013% of tokens), so it has to be measured properly rather
than inferred from a difference of two large numbers.

This times `vendor_curves()` on its own, over every page that actually reaches
it, against the wall time of the pipeline it would sit inside - both in one
process, on a warm cache, with no ordering between them to bias.

    uv run eval/curves_cost.py corpus/datasheet_holdout [--limit N]
"""
import pathlib
import statistics
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
sys.path.insert(0, str(ROOT / "eval"))
import fitz                                                   # noqa: E402
import curves_patch                                           # noqa: E402
from harvest import harvest, page_geometry, render_reason     # noqa: E402


def main(corpus, limit=None):
    patched = curves_patch.load()
    paths = sorted(pathlib.Path(corpus).glob("*.pdf"))[:limit]
    t_harvest = t_rule = 0.0
    per_page, n_pages, n_curves, fired = [], 0, 0, 0
    for p in paths:
        # The page loop runs FIRST so the timed harvest reads a warm cache.
        # Timing a second harvest against a first is what made the wall-clock
        # comparison in curves_validate.py meaningless.
        with fitz.open(str(p)) as d:
            for pg in d:
                n_pages += 1
                if render_reason(page_geometry(pg)) != "curves":
                    continue
                n_curves += 1
                t0 = time.perf_counter()
                hit = patched.vendor_curves(pg)
                dt = time.perf_counter() - t0
                t_rule += dt
                per_page.append(dt)
                fired += bool(hit)
        t0 = time.perf_counter()
        harvest(str(p))
        t_harvest += time.perf_counter() - t0
    per_page.sort()
    print(f"documents            : {len(paths)}   pages {n_pages}")
    print(f"curves pages tested  : {n_curves}   dropped {fired}")
    print(f"harvest wall (warm)  : {t_harvest:.1f}s "
          f"({1000 * t_harvest / max(1, len(paths)):.0f} ms/document)")
    print(f"vendor_curves total  : {t_rule:.1f}s "
          f"({1000 * t_rule / max(1, len(paths)):.1f} ms/document, "
          f"{100 * t_rule / t_harvest:.1f}% of harvest)")
    if per_page:
        print(f"per tested page      : median "
              f"{1000 * statistics.median(per_page):.1f} ms   p90 "
              f"{1000 * per_page[int(0.9 * len(per_page))]:.1f} ms   max "
              f"{1000 * per_page[-1]:.1f} ms")


if __name__ == "__main__":
    argv = sys.argv[1:]
    target = next((a for a in argv if not a.startswith("--")),
                  "corpus/datasheet_holdout")
    lim = int(argv[argv.index("--limit") + 1]) if "--limit" in argv else None
    main(target, lim)
