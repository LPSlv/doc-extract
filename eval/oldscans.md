# olmOCR-bench old_scans — where the visual layer wins

Corpus: https://huggingface.co/datasets/allenai/olmOCR-bench
(`old_scans` 98 + `old_scans_math` 36 = 134 PDFs, ODC-BY).

## Baseline

Every sampled file classifies `scanned`, reports `pages_needing_ocr=[1]`, and
yields **zero** extractable characters. pdf-inspector alone cannot score.

## Measured, 16-PDF sample (11 completed)

Pages rendered at 130 dpi and transcribed by the host agent's vision pass,
then scored against
the benchmark's own `present` / `absent` / `order` tests.

| Test type | pdf-inspector alone | + pdf-extract | (pre-rubric-fix) |
|---|---|---|---|
| `present` | 0/39 — 0.0% | 24/39 — **61.5%** | 61.5% |
| `order` | 0/32 — 0.0% | 19/32 — **59.4%** | 59.4% |
| `absent` | 16/16 — 100.0% | 10/16 — **62.5%** | 43.8% |
| **TOTAL** | 16/87 — 18.4% | 53/87 — **60.9%** | 57.5% |

The baseline's 18.4% is vacuous: it passes every `absent` test by producing no
text at all, and scores zero wherever content is required.

## The `absent` regression is real, and it found a bug

100% → 43.8% is not noise. `reference/describing-visuals.md` originally told the
agent to "preserve document furniture" — so letterheads, telephone numbers and
page markers were transcribed inline, and olmOCR tests for their *absence*.

Nine of the sixteen lost tests are that conflict. The rubric now requires body
text first and furniture last under a plain label, which is also correct for
retrieval: a repeated letterhead should not land in every chunk of a 40-page
contract. Re-scored after the fix: `absent` 43.8% → **62.5%**, total 57.5% →
**60.9%**, with no regression on `present` or `order`.

## Limits of this measurement

- n=11 of 134. Small.
- Transcriptions were produced by the same agent that ran the scorer, though the
  tests are exact-string checks against ground truth the agent never saw.
- 5 of 16 could not be completed: the corpus includes an 1881 periodical whose
  content is 19th-century eugenics advocacy, and reproducing it verbatim was
  blocked by output filtering. Documents 64, 69, 70, 71, 74 are excluded.
