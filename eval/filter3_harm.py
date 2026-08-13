# /// script
# requires-python = ">=3.10"
# dependencies = ["pdf-inspector==0.2.6", "pymupdf==1.28.0"]
# ///
"""Measure HARM, not exposure, on the pages filter 3 discards.

`eval/filter3.md` measures **exposure**: 65.6% of the 4,065 discarded pages
carry a real figure. Exposure is an upper bound on harm. The figures on these
pages are vector artwork, so their axis labels, tick values, legends and
captions are real text spans and most of them survive into `doc.md` --
`process_pdf` runs over the whole document regardless of routing. What the
reader loses is geometry. This asks how often that costs an *answer*.

Three arms, mirroring `eval/figqa.md`:

  closed    the question and its four options, nothing else          (floor)
  text      the whole-document markdown, i.e. the page suppressed    (STATUS QUO)
  docx      that markdown plus a description of the rendered page    (THE FIX)

plus `optical` (the page render itself), which is a ground-truth control, not
an arm: a question is only admitted if optical answers it.

THE GATE IS DELIBERATELY NOT figqa's GATE, and this is the single most
important design decision here. figqa admits a question only if the text arm
gets it WRONG, because it is measuring what the visual layer adds on pages the
router already selected. Applying that gate here would force the status-quo arm
to 0/n and "prove" harm = exposure by construction. The gate here is:

    admit iff  optical correct  AND NOT (closed correct under BOTH orderings)

i.e. the visual alone can answer it, and convention alone cannot. The text arm
is left free to succeed, because whether it succeeds *is the measurement*.

    uv run eval/filter3_harm.py select      # pick pages, three strata, seeded
    uv run eval/filter3_harm.py artifacts   # renders + whole-document markdown
    uv run eval/filter3_harm.py modes       # image-first / caption-first split
    uv run eval/filter3_harm.py merge       # authored questions -> candidates
    uv run eval/filter3_harm.py perm        # balanced key + second ordering
    uv run eval/filter3_harm.py ask         # per-arm prompt sheets
    uv run eval/filter3_harm.py score       # the gate, the table, scored.tsv
"""
import collections, csv, json, math, pathlib, random, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "eval" / "filter3_harm"
F3 = ROOT / "eval" / "filter3"

SEED = 20260814
AUTHOR_DPI = 200      # question authoring only: the oracle is never worse
                      # informed than the arm under test (figqa uses 200 too)
OPTICAL_DPI = 140     # the ground-truth control arm, as in figqa
# the describer sees the page at the edge the SHIPPED renderer would have used
# for it (harvest.render_edge, stored per row as `edge`), because that is
# literally what the fix would buy -- not a better picture.
DEFAULT_EDGE = 1000

N_S2 = 30             # out-of-sample T=4 pages (datasheet_holdout + pmc)
N_S3 = 20             # the wider blind spot, curves/diagonals


# ---------------------------------------------------------------- selection

def read_tsv(path):
    with open(path) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def strat_sample(rows, key, n, rng):
    """Proportional with a floor of one per non-empty cell, largest remainder."""
    cells = collections.defaultdict(list)
    for r in rows:
        cells[key(r)].append(r)
    names = sorted(cells)
    if n >= len(rows):
        return list(rows), [{"cell": k, "population": len(cells[k]),
                             "sampled": len(cells[k])} for k in names]
    quota = {k: 1 for k in names}
    left = n - len(names)
    if left < 0:                      # more cells than budget: keep the biggest
        names = sorted(names, key=lambda k: -len(cells[k]))[:n]
        quota = {k: 1 for k in names}
        left = 0
    rest = sum(len(cells[k]) - 1 for k in names)
    if rest > 0 and left > 0:
        share = {k: (len(cells[k]) - 1) / rest * left for k in names}
        for k in names:
            quota[k] += int(share[k])
        gap = n - sum(quota.values())
        for k in sorted(names, key=lambda k: -(share[k] % 1)):
            if gap <= 0:
                break
            if quota[k] < len(cells[k]):
                quota[k] += 1
                gap -= 1
    out, rep = [], []
    for k in names:
        take = min(quota[k], len(cells[k]))
        out += rng.sample(sorted(cells[k], key=lambda r: r["tag"]), take)
        rep.append({"cell": k, "population": len(cells[k]), "sampled": take})
    return out, rep


def select():
    rng = random.Random(SEED)
    idxA = {r["tag"]: r for r in json.loads((F3 / "index.json").read_text())["rows"]}
    A = read_tsv(F3 / "labels.tsv")
    B = read_tsv(F3 / "datasheet_holdout" / "labels.tsv")
    idxB = {r["tag"]: r for r in
            json.loads((F3 / "datasheet_holdout" / "sample.json").read_text())["rows"]}

    figA = [r for r in A if r["label"] == "figure"]
    s1 = [r for r in figA if idxA[r["tag"]]["pipe_rows"] < 4]          # census
    poolS3 = [r for r in figA if idxA[r["tag"]]["pipe_rows"] >= 4
              and r["branch"] in ("curves", "diagonals")]
    s3, rep3 = strat_sample(poolS3, lambda r: r["corpus"], N_S3, rng)

    figB = [r for r in B if r["label"] == "figure"]
    pmc = [r for r in figB if r["corpus"] == "pmc"]                    # census
    ds = [r for r in figB if r["corpus"] != "pmc"]
    s2ds, rep2 = strat_sample(ds, lambda r: r["vendor"], N_S2 - len(pmc), rng)
    s2 = pmc + s2ds

    rows = []
    for stratum, src, label in (("insample_T4", s1, "A"),
                                ("holdout_T4", s2, "B"),
                                ("blindspot", s3, "A")):
        for r in src:
            if label == "A":
                i = idxA[r["tag"]]
                doc = i["doc"]
                edge = i.get("edge") or DEFAULT_EDGE
                vendor = ""
                pipe = i["pipe_rows"]
            else:
                i = idxB[r["tag"]]
                doc = f"corpus/{'pmc' if r['corpus'] == 'pmc' else 'datasheet_holdout'}/{r['file']}"
                edge = DEFAULT_EDGE
                vendor = r["vendor"]
                pipe = int(r["pipe_rows"])
            rows.append({"stratum": stratum, "src_tag": r["tag"],
                         "corpus": r["corpus"], "vendor": vendor,
                         "doc": doc, "name": pathlib.Path(doc).name,
                         "page": int(r["page"]), "branch": r["branch"],
                         "pipe_rows": pipe, "edge": edge,
                         "label_note": r["note"]})
    rows.sort(key=lambda r: (r["stratum"], r["src_tag"]))
    for n, r in enumerate(rows):
        r["qid"] = f"h{n+1:02d}"

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "selection.json").write_text(json.dumps(
        {"seed": SEED, "author_dpi": AUTHOR_DPI, "optical_dpi": OPTICAL_DPI,
         "strata": {"insample_T4": {"census_of": len(s1)},
                    "holdout_T4": {"pmc_census": len(pmc), "by_vendor": rep2},
                    "blindspot": {"by_corpus": rep3}},
         "n": len(rows), "rows": rows}, indent=1))
    for st, g in collections.Counter(r["stratum"] for r in rows).items():
        print(f"{st:14s} {g}")
    print(f"total {len(rows)} -> {OUT/'selection.json'}")


# ---------------------------------------------------------------- artifacts

def artifacts():
    sys.path.insert(0, str(ROOT / "skills" / "doc-extract"))
    import fitz, pdf_inspector as pi
    from harvest import render_edge          # the shipped renderer's own budget
    sel = json.loads((OUT / "selection.json").read_text())["rows"]
    # One directory per arm, so no arm's material sits next to another's. The
    # text arm cannot open the page render by listing its own directory, which
    # is the only leakage control that is structural rather than an instruction.
    for sub in ("pages", "mat_optical", "mat_render", "mat_text", "mat_docx", "view"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    cache, mismatch = {}, 0
    for r in sel:
        d = OUT / "mat_docx" / r["qid"]
        d.mkdir(parents=True, exist_ok=True)
        doc_path = str(ROOT / r["doc"])
        with fitz.open(doc_path) as doc:
            pg = doc[r["page"] - 1]
            pg.get_pixmap(dpi=AUTHOR_DPI).save(str(OUT / "pages" / f"{r['qid']}.png"))
            pg.get_pixmap(dpi=OPTICAL_DPI).save(
                str(OUT / "mat_optical" / f"{r['qid']}.png"))
            # exactly what the fix would render: the long edge the SHIPPED
            # renderer would pick for this page, not a better picture. For
            # stratum A the enumeration already stored it; recomputing and
            # diffing is a free cross-check against a file written elsewhere.
            edge = render_edge(pg)
            if r["edge"] != DEFAULT_EDGE and edge != r["edge"]:
                print(f"   !! {r['qid']} render_edge {edge} != stored {r['edge']}")
                mismatch += 1
            r["edge"] = edge
            s = edge / max(pg.rect.width, pg.rect.height)
            pg.get_pixmap(matrix=fitz.Matrix(s, s)).save(
                str(OUT / "mat_render" / f"{r['qid']}.png"))
            # authoring only, never graded: the page's own text layer. The
            # caption-first authors see this and NOT the picture, so the topic
            # of half the questions is chosen without knowing what the image
            # holds -- the control on authorship bias.
            (OUT / "view" / f"{r['qid']}.txt").write_text(pg.get_text())
        if doc_path not in cache:
            cache[doc_path] = pi.process_pdf(doc_path).markdown or ""
        (OUT / "mat_text" / f"{r['qid']}.md").write_text(cache[doc_path])
        print(f"{r['qid']}  {r['name'][:34]:34s} p{r['page']:<4d} "
              f"edge {edge:<5d} md {len(cache[doc_path]):7d}")
    print(f"render_edge mismatches against eval/filter3/index.json: {mismatch}")
    blob = json.loads((OUT / "selection.json").read_text())
    blob["rows"] = sel
    (OUT / "selection.json").write_text(json.dumps(blob, indent=1))


def modes():
    """Assign each page an authoring mode, seeded, balanced inside each stratum.

    THE AUTHORSHIP-BIAS CONTROL. An author who writes a question while looking
    at a figure is selecting for facts a picture carries, which is exactly the
    quantity under test. So half the pages are authored the other way round:

      image-first    the author sees the 200 dpi page render and nothing else,
                     and writes the question a reader would most want answered
      caption-first  one author sees ONLY the page's own text layer -- caption,
                     surrounding prose, whatever axis labels survived -- and
                     with no picture at all writes the QUESTION STEM. A second
                     author then reads the render and supplies the four options
                     and the key. The topic is therefore chosen by someone who
                     could not know whether the text answers it.

    The two modes are scored separately. If image-first shows materially more
    harm than caption-first, the gap IS the authorship bias, measured.
    """
    blob = json.loads((OUT / "selection.json").read_text())
    rng = random.Random(SEED + 2)
    for st in ("insample_T4", "holdout_T4", "blindspot"):
        g = [r for r in blob["rows"] if r["stratum"] == st]
        order = list(range(len(g)))
        rng.shuffle(order)
        for pos, k in enumerate(order):
            g[k]["mode"] = "image_first" if pos % 2 == 0 else "caption_first"
    (OUT / "selection.json").write_text(json.dumps(blob, indent=1))
    print(collections.Counter((r["stratum"], r["mode"]) for r in blob["rows"]))


def merge():
    """Collect the authored questions into one candidate set, with withdrawals.

    `withdrawn.json` is a list of {"id", "reason"} and is applied HERE rather
    than by deleting the question, so a withdrawal is auditable. figqa withdrew
    v25 the same way and says so; a quietly deleted question is indistinguishable
    from one that never existed.
    """
    sel = {r["qid"]: r for r in json.loads((OUT / "selection.json").read_text())["rows"]}
    withdrawn = {}
    p = OUT / "withdrawn.json"
    if p.exists():
        withdrawn = {r["id"]: r["reason"] for r in json.loads(p.read_text())}

    got, dropped = {}, []
    for f in sorted((OUT / "authored").glob("img-b*.json")) + \
             sorted((OUT / "authored").glob("cap-b*.json")):
        for r in json.loads(f.read_text()):
            i = r["id"]
            if i in got:
                raise SystemExit(f"{i} authored twice ({f})")
            if r.get("answerable") is False:
                dropped.append((i, "author: page cannot settle the stem"))
                continue
            if i in withdrawn:
                dropped.append((i, "withdrawn: " + withdrawn[i]))
                continue
            got[i] = {"id": i, "q": r["q"], "options_raw": r["options_raw"],
                      "kind": r.get("kind", ""), "fact": r.get("fact", ""),
                      "why_arbitrary": r.get("why_arbitrary", ""),
                      "stem_edit": r.get("stem_edit", ""),
                      "mode": sel[i]["mode"], "stratum": sel[i]["stratum"],
                      "source_page": f"{sel[i]['doc']} p{sel[i]['page']}",
                      "branch": sel[i]["branch"], "src_tag": sel[i]["src_tag"]}
    absent = [q for q in sel if q not in got and q not in dict(dropped)]
    if absent:
        print("!! no question authored for:", absent)
    cands = [got[i] for i in sorted(got, key=lambda x: int(x[1:]))]
    (OUT / "candidates.json").write_text(json.dumps(
        {"n_pages": len(sel), "n_candidates": len(cands),
         "dropped": [{"id": i, "why": w} for i, w in dropped],
         "candidates": cands}, indent=1))
    print(f"{len(cands)} candidates, {len(dropped)} dropped")
    for i, w in dropped:
        print(f"  {i}: {w}")
    print(collections.Counter((c["mode"], c["kind"]) for c in cands))


# ---------------------------------------------------------------- key + perm

def perm():
    """Build the answer key with balanced positions, and a second ordering.

    figqa put the correct option at C in 14 of 30 and a guessing arm scored 8/10
    on that group. Here the key position is assigned by a seeded round-robin
    over a shuffled question order, so every arm's guessing rate is 25% by
    construction, and `score` checks the realised distribution.
    """
    cands = json.loads((OUT / "candidates.json").read_text())["candidates"]
    for c in cands:                     # the key comes from options_raw[0] and
        o = c["options_raw"]            # nothing else, so malformed input must
        if len(o) != 4 or len(set(o)) != 4:      # not pass silently
            raise SystemExit(f"{c['id']}: options_raw is {o!r}, need 4 distinct")
    rng = random.Random(SEED + 1)
    ids = [c["id"] for c in cands]
    rng.shuffle(ids)
    slot = {}
    for n, i in enumerate(ids):
        slot[i] = n % 4
    out = {}
    for c in cands:
        # authors write options with the correct one first; place it at `slot`
        opts = list(c["options_raw"])
        correct = opts[0]
        rest = opts[1:]
        rng.shuffle(rest)
        placed = rest[:slot[c["id"]]] + [correct] + rest[slot[c["id"]]:]
        # second ordering for the closed-book re-run: a derangement of the
        # first, so position luck cannot disqualify a good question twice
        alt = placed[1:] + placed[:1]
        out[c["id"]] = {"options": placed, "answer": correct,
                        "key": chr(65 + placed.index(correct)),
                        "alt_options": alt,
                        "alt_key": chr(65 + alt.index(correct))}
    (OUT / "perm.json").write_text(json.dumps(out, indent=1))
    dist = collections.Counter(v["key"] for v in out.values())
    print("key positions:", dict(sorted(dist.items())))
    dist2 = collections.Counter(v["alt_key"] for v in out.values())
    print("alt positions:", dict(sorted(dist2.items())))


def ask():
    """Write the per-arm prompt sheets. No arm sheet reveals another's material."""
    sel = {r["qid"]: r for r in json.loads((OUT / "selection.json").read_text())["rows"]}
    cands = json.loads((OUT / "candidates.json").read_text())["candidates"]
    perm = json.loads((OUT / "perm.json").read_text())
    (OUT / "ask").mkdir(parents=True, exist_ok=True)

    def opts(i, alt=False):
        o = perm[i]["alt_options" if alt else "options"]
        return " | ".join(f"({chr(65+n)}) {t}" for n, t in enumerate(o))

    batches = collections.defaultdict(list)
    for n, c in enumerate(cands):
        batches[n // 12 + 1].append(c)

    # Each arm is pointed at its OWN directory. mat_text holds no images and
    # mat_optical holds no markdown, so an arm cannot reach another arm's
    # material by listing the directory it was given.
    mats = {"optical": ["{OUT}/mat_optical/{id}.png"],
            "text": ["{OUT}/mat_text/{id}.md"],
            "docx": ["{OUT}/mat_text/{id}.md",
                     "{OUT}/mat_docx/{id}/description.md"]}
    for arm, alt in (("optical", False), ("text", False), ("docx", False)):
        for b, group in sorted(batches.items()):
            lines = []
            for c in group:
                lines.append(f"### {c['id']}")
                for m in mats[arm]:
                    lines.append("Material: " + m.format(OUT=OUT, id=c["id"]))
                if arm in ("text", "docx"):
                    # The shipped artifact carries pages/pNNN.md beside doc.md,
                    # so a real reader always knows which page to look at.
                    # Withholding it would manufacture a "could not find it"
                    # failure that the status quo does not actually have.
                    lines.append(f"The figure is on page {sel[c['id']]['page']} "
                                 f"of the document.")
                lines.append(f"Question: {c['q']}")
                lines.append(f"Options: {opts(c['id'], alt)}")
                lines.append("")
            (OUT / "ask" / f"{arm}-b{b}.md").write_text("\n".join(lines))
    # the closed-book arm has no materials, so one sheet with everything is fine
    for arm, alt in (("closed", False), ("closed2", True)):
        lines = []
        for c in cands:
            lines += [f"### {c['id']}", f"Question: {c['q']}",
                      f"Options: {opts(c['id'], alt)}", ""]
        (OUT / "ask" / f"{arm}-all.md").write_text("\n".join(lines))
    print(f"wrote {len(batches)} batches x 3 material arms + 2 closed sheets "
          f"-> {OUT/'ask'}")


# ---------------------------------------------------------------- scoring

def wilson(k, n, z=1.96):
    if not n:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def load_arm(prefix):
    got = {}
    for p in sorted((OUT / "answers").glob(f"{prefix}-*.json")):
        for row in json.loads(p.read_text()):
            if row["id"] in got:
                raise SystemExit(f"duplicate answer for {row['id']} in {p}")
            got[row["id"]] = row
    return got


def verify():
    """Check the arms actually read what they were given.

    The text arm is graded on `grounded`, and `grounded` is the arm's own
    claim. This audits it mechanically: every quote a grounded text answer
    rests on must really occur in that question's markdown. A quote that does
    not occur is either a paraphrase (weak evidence) or a fabrication (a
    grounded credit the arm did not earn) -- and, if it turned out to be a
    string only visible on the page, it would be leakage.

    Also checks the docx arm's description-sourced quotes against the
    description file, and reports how much of each arm's material actually
    exists.
    """
    def norm(s):
        return " ".join((s or "").split()).lower()

    problems = []
    for prefix, files in (("text", lambda i: [OUT / "mat_text" / f"{i}.md"]),
                          ("docx", lambda i: [OUT / "mat_text" / f"{i}.md",
                                              OUT / "mat_docx" / i / "description.md"])):
        arm = load_arm(prefix)
        n = ok = para = 0
        for i, r in sorted(arm.items()):
            if not r.get("grounded"):
                continue
            q = norm(r.get("quote"))
            if not q:
                problems.append((prefix, i, "grounded with no quote"))
                continue
            n += 1
            hay = " ".join(norm(p.read_text()) for p in files(i) if p.exists())
            if q in hay:
                ok += 1
                continue
            # a quote assembled from several places, or lightly reflowed:
            # accept if every run of >=5 words occurs somewhere in the material
            words = q.split()
            runs = [" ".join(words[k:k + 5]) for k in range(0, max(1, len(words) - 4))]
            hit = sum(1 for run in runs if run in hay)
            if runs and hit / len(runs) >= 0.5:
                para += 1
            else:
                problems.append((prefix, i, f"quote not in material ({hit}/{len(runs)} runs): "
                                            f"{(r.get('quote') or '')[:90]!r}"))
        print(f"{prefix:6s} grounded answers {n:3d}   verbatim {ok:3d}   "
              f"reflowed/assembled {para:3d}   unverified {n - ok - para:3d}")
    print()
    if problems:
        print("UNVERIFIED GROUNDING CLAIMS — each one is a grounded credit the arm may not have earned:")
        for p in problems:
            print("  ", *p)
    else:
        print("every grounded claim traces to the arm's own material")


def score(as_json=False):
    sel = {r["qid"]: r for r in json.loads((OUT / "selection.json").read_text())["rows"]}
    cands = {c["id"]: c for c in json.loads((OUT / "candidates.json").read_text())["candidates"]}
    perm = json.loads((OUT / "perm.json").read_text())
    screen = {}
    p = OUT / "screen.json"
    if p.exists():
        screen = {r["id"]: r for r in json.loads(p.read_text())}

    # The key must agree with the authored options and with the sheet the arms
    # were actually shown. figqa's fourth harness defect was a scorer reading
    # the wrong column; this asserts the columns line up before anything scores.
    for i, c in cands.items():
        pm = perm[i]
        assert pm["answer"] == c["options_raw"][0], f"{i}: answer drifted"
        assert pm["options"][ord(pm["key"]) - 65] == pm["answer"], f"{i}: key wrong"
        assert pm["alt_options"][ord(pm["alt_key"]) - 65] == pm["answer"], f"{i}: alt key wrong"
        assert sorted(pm["options"]) == sorted(c["options_raw"]), f"{i}: options drifted"
        assert pm["key"] != pm["alt_key"], f"{i}: second ordering is not a move"

    arms = {n: load_arm(n) for n in ("closed", "closed2", "optical", "text", "docx")}
    for n, a in arms.items():
        miss = [i for i in cands if i not in a]
        extra = [i for i in a if i not in cands]
        if miss:
            print(f"!! {n} unanswered: {miss}")
        if extra:
            print(f"!! {n} answered ids that are not candidates: {extra}")

    unparsed = []

    def correct(arm, i, alt=False):
        r = arms[arm].get(i)
        if not r:
            return None
        raw = (r.get("choice") or "").strip().upper()
        ch = raw[:1] if raw[:1] in "ABCD" else ""
        if not ch:                       # an arm that answered with the option
            opts = perm[i]["alt_options" if alt else "options"]   # text, not a letter
            for n, t in enumerate(opts):
                if t.strip().upper() == raw:
                    ch = chr(65 + n)
            if not ch:
                unparsed.append((arm, i, r.get("choice")))
                return None
        return ch == perm[i]["alt_key" if alt else "key"]

    # --- positional bias check on the realised key, and on each arm's answers
    keydist = collections.Counter(perm[i]["key"] for i in cands)
    print("key position distribution:", dict(sorted(keydist.items())))
    for n in arms:
        d = collections.Counter((arms[n].get(i, {}).get("choice") or "?").strip().upper()[:1]
                                for i in cands)
        print(f"  {n:8s} chose:", dict(sorted(d.items())))
    print()

    rows = []
    for i, c in cands.items():
        fair = screen.get(i, {}).get("fair")
        r = {"id": i, "stratum": sel[i]["stratum"], "mode": sel[i]["mode"],
             "corpus": sel[i]["corpus"], "vendor": sel[i]["vendor"],
             "name": sel[i]["name"], "page": sel[i]["page"], "branch": sel[i]["branch"],
             "key": perm[i]["key"],
             # the screener's classification, not the author's: the author had
             # a stake in the answer and the screener did not. They disagree on
             # 5 of 69, always author-`printed` vs screener-`geometry`.
             "kind": screen.get(i, {}).get("kind") or c.get("kind", ""),
             "kind_author": c.get("kind", ""),
             "relevance": screen.get(i, {}).get("relevance", ""),
             "fair": fair, "fair_reason": screen.get(i, {}).get("reason", ""),
             "optical": correct("optical", i),
             "optical_grounded": bool(arms["optical"].get(i, {}).get("grounded")),
             "closed": correct("closed", i), "closed2": correct("closed2", i, alt=True),
             "text": correct("text", i), "docx": correct("docx", i),
             "text_grounded": bool(arms["text"].get(i, {}).get("grounded")),
             "docx_grounded": bool(arms["docx"].get(i, {}).get("grounded"))}
        conv = bool(r["closed"]) and bool(r["closed2"])
        r["convention"] = conv
        r["admitted"] = bool(r["optical"]) and not conv and (fair is not False)
        rows.append(r)
    rows.sort(key=lambda r: r["id"])

    if unparsed:
        print("!! unparseable choices:", unparsed)
    adm = [r for r in rows if r["admitted"]]
    print(f"candidates {len(rows)}  |  ground truth unsound (optical wrong) "
          f"{sum(1 for r in rows if not r['optical'])}  |  reachable by convention "
          f"{sum(1 for r in rows if r['convention'])}  |  screened unfair "
          f"{sum(1 for r in rows if r['fair'] is False)}  |  ADMITTED {len(adm)}")
    print()

    def block(title, sub):
        n = len(sub)
        if not n:
            return
        t = sum(1 for r in sub if r["text"])
        tg = sum(1 for r in sub if r["text"] and r["text_grounded"])
        d = sum(1 for r in sub if r["docx"])
        # LOST is the harm floor: the status-quo arm got it wrong outright.
        # LOST_g additionally counts answers it got right without being able
        # to point at the line that says so -- at a balanced 4-option key,
        # guessing scores 25%, and figqa's v2 was misread exactly this way.
        lost = sum(1 for r in sub if not r["text"])
        lostg = sum(1 for r in sub if not (r["text"] and r["text_grounded"]))
        rec = sum(1 for r in sub if not r["text"] and r["docx"])
        lo, hi = wilson(lost, n)
        glo, ghi = wilson(lostg, n)
        rlo, rhi = wilson(rec, n)
        print(f"{title:26s} n={n:<4d} text {t:>3} ({t/n:5.1%}) gr {tg:>3}  "
              f"docx {d:>3} ({d/n:5.1%})  "
              f"LOST {lost:>3} ({lost/n:5.1%}, {lo:.0%}-{hi:.0%})  "
              f"LOST_g {lostg:>3} ({lostg/n:5.1%}, {glo:.0%}-{ghi:.0%})  "
              f"fix recovers {rec:>3} ({rec/n:5.1%}, {rlo:.0%}-{rhi:.0%})")

    # TWO DENOMINATORS, and the difference between them is a finding, not a
    # technicality.
    #
    #   `sound`    every question the page itself settles. A question the
    #              closed-book arm can also answer is a question the reader
    #              does NOT lose when the page is suppressed -- zero harm --
    #              so for a HARM measurement it belongs in the denominator.
    #              This is the product-relevant rate: the arms are the same
    #              model that reads documents in production, so its priors are
    #              the user's priors.
    #   `admitted` additionally drops the convention-reachable ones, mirroring
    #              figqa's gate. This isolates what the PAGE uniquely carries
    #              and is the contamination-free number, at a smaller n.
    sound = [r for r in rows if r["optical"] and r["fair"] is not False]
    print("harm over ALL sound questions — convention-reachable ones count as "
          "no-harm, because the reader answers them anyway")
    print("-" * 150)
    block("ALL sound", sound)
    for st in ("insample_T4", "holdout_T4", "blindspot"):
        block(f"  {st}", [r for r in sound if r["stratum"] == st])
    for k in sorted({r["kind"] for r in sound if r["kind"]}):
        block(f"  kind {k}", [r for r in sound if r["kind"] == k])
    for m in sorted({r["mode"] for r in sound}):
        block(f"  authored {m}", [r for r in sound if r["mode"] == m])
    print()
    print("harm on ADMITTED questions (page-only facts: convention cannot reach them)")
    print("-" * 150)
    block("ALL", adm)
    for st in ("insample_T4", "holdout_T4", "blindspot"):
        block(f"  {st}", [r for r in adm if r["stratum"] == st])
    for cp in sorted({r["corpus"] for r in adm}):
        block(f"  corpus {cp}", [r for r in adm if r["corpus"] == cp])
    for k in sorted({r["kind"] for r in adm if r["kind"]}):
        block(f"  kind {k}", [r for r in adm if r["kind"] == k])
    for m in sorted({r["mode"] for r in adm}):
        block(f"  authored {m}", [r for r in adm if r["mode"] == m])
    print()
    closed_all = [r for r in rows if r["closed"]]
    print(f"floor: closed-book {len(closed_all)}/{len(rows)} on candidates, "
          f"{sum(1 for r in adm if r['closed'])}/{len(adm)} on admitted "
          f"(forced <all>, since admission requires failing both orderings)")

    hdr = ["id", "stratum", "mode", "corpus", "vendor", "name", "page", "branch",
           "kind", "kind_author", "relevance",
           "key", "fair", "fair_reason", "optical", "optical_grounded",
           "closed", "closed2", "convention",
           "admitted", "text", "text_grounded", "docx", "docx_grounded"]
    with open(OUT / "scored.tsv", "w") as fh:
        w = csv.DictWriter(fh, fieldnames=hdr, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nwrote {OUT/'scored.tsv'}")
    if as_json:
        (OUT / "scored.json").write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "score"
    {"select": select, "artifacts": artifacts, "modes": modes, "merge": merge,
     "perm": perm, "ask": ask, "verify": verify,
     "score": lambda: score("--json" in sys.argv)}[cmd]()
