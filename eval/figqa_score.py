# /// script
# requires-python = ">=3.10"
# ///
"""Score the three figure-QA arms and print the comparison table.

Grading is a letter match against questions.json — no judgement at scoring
time, which is the point of having used multiple choice. Random baseline is
25%, and it is printed alongside so a weak arm is not mistaken for a zero.

    uv run eval/figqa_score.py [--json]
"""
import json, pathlib, sys, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "eval" / "figqa"
ARMS = [("text", "pdf-inspector text only"),
        ("docx", "doc-extract (text + routed figures)"),
        ("optical", "full optical (page render)")]


def load_arm(prefix):
    got = {}
    for g in ("g1", "g2", "g3"):
        p = OUT / "answers" / f"{prefix}-{g}.json"
        if not p.exists():
            continue
        for row in json.loads(p.read_text()):
            got[row["id"]] = row
    return got


def main(as_json=False):
    spec = json.loads((OUT / "questions.json").read_text())
    qs = spec["questions"]
    key = {}
    for q in qs:
        key[q["id"]] = chr(65 + q["options"].index(q["answer"]))

    results, per_q = {}, collections.defaultdict(dict)
    for prefix, label in ARMS:
        got = load_arm(prefix)
        hit = miss = absent = 0
        grounded_hit = 0
        for q in qs:
            r = got.get(q["id"])
            if r is None:
                absent += 1
                per_q[q["id"]][prefix] = "-"
                continue
            ok = (r.get("choice") or "").strip().upper()[:1] == key[q["id"]]
            hit += ok
            miss += not ok
            grounded_hit += bool(ok and r.get("grounded"))
            per_q[q["id"]][prefix] = "hit" if ok else "MISS"
        results[prefix] = {"label": label, "n": len(qs), "answered": len(qs) - absent,
                           "correct": hit, "wrong": miss, "missing": absent,
                           "grounded_correct": grounded_hit}

    if as_json:
        print(json.dumps({"per_arm": results, "per_question": per_q}, indent=1))
        return

    n = len(qs)
    print(f"Figure-QA: {n} questions, 4 options each, random baseline {100/4:.0f}%\n")
    w = max(len(v["label"]) for v in results.values())
    print(f"{'arm':<{w}}  correct   share   grounded")
    print("-" * (w + 28))
    for prefix, _ in ARMS:
        r = results[prefix]
        share = r["correct"] / n * 100 if n else 0
        note = f"  ({r['missing']} unanswered)" if r["missing"] else ""
        print(f"{r['label']:<{w}}  {r['correct']:>3}/{n:<3}  {share:5.1f}%   "
              f"{r['grounded_correct']:>3}{note}")

    print("\nper question:")
    hdr = "".join(f"{p:>10}" for p, _ in ARMS)
    print(f"{'id':<6}{hdr}")
    for q in qs:
        row = "".join(f"{per_q[q['id']].get(p,'-'):>10}" for p, _ in ARMS)
        print(f"{q['id']:<6}{row}")


if __name__ == "__main__":
    main("--json" in sys.argv)
