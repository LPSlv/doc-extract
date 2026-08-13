# The instruction every labeller was given

Verbatim, so a third party can judge whether the labels were led. Each of the
three labellers received exactly this text, saw only the PNGs, and could not
see each other's answers, the rule, the hypothesis, or which answer would be
convenient. The output path was the only difference between them.

---

You are classifying rendered pages from PDF component datasheets. Look at each
image and say what is on that page.

The images are `/home/lps/pdf-extract/eval/curves_holdout/pages/<tag>.png`. The
tags you must label are listed in
`/home/lps/pdf-extract/eval/curves_holdout/batch.tsv`. Label EVERY tag in that
file, exactly once.

Read the PNGs and nothing else. Do not read any other file in the repository —
not the JSON indexes in that directory, not anything under `eval/*.md`, not the
skill's source. They contain the hypothesis being tested and would tell you
which answer is convenient. Do not open the source PDFs.

For each page choose ONE label:

- `figure` — the page carries something a reader would need to SEE: a chart or
  plot, a characteristic curve, a schematic, a block or timing diagram, a
  pinout, a package/mechanical drawing, a waveform, a photograph, an
  illustration, an oscilloscope capture, a layout or footprint drawing.
- `table` — the page carries real tabular data: a parameter table, an
  electrical-characteristics table, a register map, an ordering-information
  table, a pin-description table.
- `branding` — the only non-text graphics on the page are vendor or publisher
  furniture: a company logo, a header or footer rule, a page border, a
  watermark, a QR code, a certification or RoHS mark, a decorative bar.
- `none` — nothing graphical at all. Prose, legal text, a revision history in
  plain paragraphs, an index; no logo, no rules, no marks.

**Break every tie towards `figure` or `table`.** If you are unsure whether
something is a real figure or just furniture, call it a figure. If a page holds
both a real figure and a logo, it is `figure`. Only use `branding` or `none`
when you are confident there is nothing on the page worth looking at.

Write your answers to
`/home/lps/pdf-extract/eval/curves_holdout/labels-<batch><a|b|c>.tsv`
as tab-separated values with the header `tag<TAB>label<TAB>note`, one row per
tag, where `note` is a short description of what you actually saw (a few
words). Emit exactly one row per tag in your batch file and no others.
