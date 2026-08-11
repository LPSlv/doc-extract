# /// script
# requires-python = ">=3.10"
# ///
"""Apply v2's screening gate and report which candidates survive it.

A candidate is ADMITTED only if all three hold:

  optical  correct  - the page really does settle it, so ground truth is sound
  closed   wrong    - not reachable from convention or world knowledge
  text     wrong    - not in the whole-document markdown, as prose OR as the
                      scrambled token runs that figure labels decay into

The closed-book arm is run TWICE, under different option orderings, and a
candidate is only called convention-reachable if it is answered correctly
BOTH times. v1's key had the answer at position C in 14 of 30 questions and a
guessing arm picked B or C 24 times out of 30; requiring agreement across two
permutations is what stops that position luck from silently disqualifying good
questions.

    uv run eval/figqa_v2_screen.py
"""
import json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "eval" / "figqa"


def load(prefix, groups):
    got = {}
    for g in groups:
        p = OUT / "answers" / f"{prefix}-{g}.json"
        if p.exists():
            for r in json.loads(p.read_text()):
                got[r["id"]] = r
    return got


def choice_text(cand, letter, order=None):
    """Resolve a letter to the option text it referred to on that arm's sheet."""
    if not letter:
        return None
    i = ord(letter.strip().upper()[0]) - 65
    opts = [cand["options"][k] for k in order] if order else cand["options"]
    return opts[i] if 0 <= i < len(opts) else None


def main():
    cands = json.loads((OUT / "v2-candidates.json").read_text())["candidates"]
    perm = json.loads((OUT / "v2-perm.json").read_text())

    closed1 = load("v-closed", ["g1", "g2", "g3"])
    closed2 = load("v-closed2", ["s1", "s2", "s3"])
    text = load("v-text", ["g1", "g2", "g3"])
    opt = load("v-optical", ["g1", "g2", "g3"])

    rows, admitted = [], []
    missing = collections.Counter()
    for c in cands:
        i = c["id"]
        for name, arm in (("closed1", closed1), ("closed2", closed2),
                          ("text", text), ("optical", opt)):
            if i not in arm:
                missing[name] += 1
        c1 = choice_text(c, closed1.get(i, {}).get("choice")) == c["answer"]
        c2 = choice_text(c, closed2.get(i, {}).get("choice"), perm[i]) == c["answer"]
        tr = text.get(i, {})
        o = choice_text(c, opt.get(i, {}).get("choice")) == c["answer"]

        # "In the text" means the arm FOUND it, not that it guessed the right
        # letter. Ungrounded hits ran 11/17 against ~4.2 expected, because the
        # original key put the answer at C in 14 of 30 - the same position bias
        # the second closed-book permutation exists to defeat. Grounded claims
        # are reliable (12/13 correct) and carry a quoted snippet.
        t = choice_text(c, tr.get("choice")) == c["answer"] and bool(tr.get("grounded"))

        conventional = c1 and c2
        ok = o and not conventional and not t
        rows.append((i, c["src"], o, c1, c2, t, ok))
        if ok:
            admitted.append(c)

    if missing:
        print("WARNING - arms with unanswered candidates:", dict(missing), "\n")

    print(f"{'id':<5}{'src':<6}{'optical':>9}{'closed1':>9}{'closed2':>9}"
          f"{'text':>7}{'admitted':>10}")
    print("-" * 55)
    m = lambda b: "ok" if b else "-"
    for i, src, o, c1, c2, t, ok in rows:
        print(f"{i:<5}{src:<6}{m(o):>9}{m(c1):>9}{m(c2):>9}{m(t):>7}"
              f"{('YES' if ok else ''):>10}")

    n = len(rows)
    print()
    print(f"candidates              : {n}")
    print(f"  optical wrong (bad Q) : {sum(1 for r in rows if not r[2])}")
    print(f"  conventional          : {sum(1 for r in rows if r[3] and r[4])}")
    print(f"  in the extracted text : {sum(1 for r in rows if r[5])}")
    print(f"  ADMITTED              : {len(admitted)}")

    (OUT / "v2-admitted.json").write_text(json.dumps(
        {"screening": "optical correct AND NOT(closed1 AND closed2) AND text wrong",
         "n_candidates": n, "n_admitted": len(admitted),
         "admitted": admitted}, indent=1))


if __name__ == "__main__":
    main()
