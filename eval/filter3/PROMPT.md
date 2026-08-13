# The labelling instruction, verbatim

Every labeller was given exactly this text plus one batch file, and nothing
else — no file names, no corpus, no page numbers, no statement of what the
answer would be used for and no indication of which answer is convenient.

The tie-break is deliberately set *against* the hypothesis being tested: these
pages are currently skipped, routing one costs money, so a labeller who is
unsure is told to say the page has no figure.

---

You are labelling page images. Each PNG is one whole page of a PDF document,
rendered at 130 dpi. Nothing has been drawn or marked on it.

Read every image listed in the batch file, one at a time, in order. Then emit
one row per image.

Context you need, and it is all the context there is:

- The page's running text, headings, captions and any ruled table are already
  recovered separately as plain text and Markdown. Text and tables are
  therefore **not** a loss if nobody ever looks at this page as an image.
- Looking at the page is only worth paying for if it carries **graphics**:
  charts, plots, diagrams, schematics, circuit drawings, waveforms,
  oscilloscope traces, photographs, micrographs, maps, timing diagrams,
  package or mechanical drawings, illustrations — anything whose meaning
  requires seeing it.

Label each page with exactly one of:

- `figure` — the page carries at least one real graphic, as defined above.
- `table` — the only non-text content is one or more tables (ruled, shaded or
  plain). No graphic anywhere on the page.
- `branding` — the only non-text content is logos, vendor marks, publisher
  banners, QR codes, header or footer rules, borders, or other page furniture.
- `none` — nothing but text: prose, headings, lists, equations, code,
  references.

Rules for the hard cases:

- A ruled or shaded table is `table`, however elaborate, and however much its
  ruling resembles a drawing.
- Mathematical display equations, however elaborate, are not graphics. `none`.
- Company logos, publisher banners, small icons, QR codes, header/footer rules
  and page decorations are never `figure`. If they are the only non-text
  content on the page, `branding`.
- A pin-out drawing, a package outline, a block diagram, a schematic, a
  plotted curve, a photograph or a waveform is `figure` even when small.
- If a page carries both a table and a graphic, label `figure`.
- **Break every tie away from `figure`.** If you are unsure whether something
  is a real graphic or merely ruling, layout or decoration, do not say
  `figure`.

Output a TSV file at the path you are given, with exactly this header:

    tag	label	note

One row per image, in batch order. `note` is a short phrase, at most twelve
words, naming what is on the page. Write nothing else into the file.
