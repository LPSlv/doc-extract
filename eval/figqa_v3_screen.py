# /// script
# requires-python = ">=3.10"
# ///
"""Screen v3 and score the one arm the gate does not constrain.

Same gate as v2 (`figqa_v2_screen.py`), applied to a set built to remove v2's
three construction weaknesses: the questions were authored by agents that saw
only page renders, every routed item is a cropped raster rather than a
whole-page render, and the answer key is balanced 10/10/10/10.

Admit iff:
  optical correct                     ground truth sound, page settles it
  NOT (closed1 AND closed2)           not reachable by convention, tested
                                      under two option orderings so position
                                      luck cannot disqualify a good question
  NOT (text correct AND grounded)     not recoverable from the markdown

Then report doc-extract on the admitted set. The other three arms score what
admission forces; only doc-extract is free to fail.

    uv run eval/figqa_v3_screen.py
"""
import json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
V3 = ROOT / "eval" / "figqa" / "v3"


def load(*names):
    got = {}
    for n in names:
        p = V3 / n
        if p.exists():
            for r in json.loads(p.read_text()):
                got[r["id"]] = r
    return got


def pick(c, letter, order=None):
    if not letter:
        return None
    i = ord(letter.strip().upper()[0]) - 65
    opts = [c["options"][k] for k in order] if order else c["options"]
    return opts[i] if 0 <= i < len(opts) else None


def main():
    cands = json.loads((V3 / "candidates.json").read_text())["candidates"]
    perm = json.loads((V3 / "perm.json").read_text())

    closed1 = load("answers-closed-k12.json", "answers-closed-k34.json")
    closed2 = load("answers-closed2-s12.json", "answers-closed2-s34.json")
    text = load("answers-text-k12.json", "answers-text-k34.json")
    opt = load("answers-optical-k12.json", "answers-optical-k34.json")
    docx = load("answers-docx-k12.json", "answers-docx-k34.json")

    missing = {n: sum(1 for c in cands if c["id"] not in a)
               for n, a in (("closed1", closed1), ("closed2", closed2),
                            ("text", text), ("optical", opt), ("doc-extract", docx))}
    if any(missing.values()):
        print("arms with unanswered candidates:", {k: v for k, v in missing.items() if v}, "\n")

    rows, admitted = [], []
    for c in cands:
        i = c["id"]
        c1 = pick(c, closed1.get(i, {}).get("choice")) == c["answer"]
        c2 = pick(c, closed2.get(i, {}).get("choice"), perm[i]) == c["answer"]
        tr = text.get(i, {})
        t = pick(c, tr.get("choice")) == c["answer"] and bool(tr.get("grounded"))
        o = pick(c, opt.get(i, {}).get("choice")) == c["answer"]
        ok = o and not (c1 and c2) and not t
        rows.append((i, o, c1, c2, t, ok))
        if ok:
            admitted.append(c)

    m = lambda b: "ok" if b else "-"
    print(f"{'id':<7}{'optical':>9}{'closed1':>9}{'closed2':>9}{'text':>7}{'admitted':>10}")
    print("-" * 51)
    for i, o, c1, c2, t, ok in rows:
        print(f"{i:<7}{m(o):>9}{m(c1):>9}{m(c2):>9}{m(t):>7}{('YES' if ok else ''):>10}")

    n = len(rows)
    conv = sum(1 for r in rows if r[2] and r[3])
    intext = sum(1 for r in rows if r[4])
    both = sum(1 for r in rows if r[2] and r[3] and r[4])
    print()
    print(f"candidates                  : {n}")
    print(f"  ground truth unsound      : {sum(1 for r in rows if not r[1])}")
    print(f"  reachable by convention   : {conv}")
    print(f"  recoverable from the text : {intext}   (overlap with above: {both})")
    print(f"  ADMITTED                  : {len(admitted)}")

    if admitted and docx:
        hit = sum(1 for c in admitted if pick(c, docx.get(c["id"], {}).get("choice")) == c["answer"])
        gr = sum(1 for c in admitted if docx.get(c["id"], {}).get("grounded"))
        miss = [c["id"] for c in admitted
                if pick(c, docx.get(c["id"], {}).get("choice")) != c["answer"]]
        print()
        print(f"doc-extract on the admitted set: {hit}/{len(admitted)} correct, {gr} grounded")
        if miss:
            print(f"  MISSED: {', '.join(miss)}")
        pages = collections.Counter(c["page_img"] for c in admitted)
        print(f"  spread: {len(pages)} distinct pages, max {max(pages.values())} questions from one")

    (V3 / "admitted.json").write_text(json.dumps(
        {"n_candidates": n, "n_admitted": len(admitted), "admitted": admitted}, indent=1))


if __name__ == "__main__":
    main()
