# The labelling instruction, verbatim

Every labeller was given exactly this text plus one batch file, and nothing
else — no file names, no corpus, no page numbers, no statement of what the
answer would be used for and no indication of which answer is convenient.

---

You are labelling page images. Each PNG is one page of a PDF document,
rendered whole. **One or more red rectangles** are drawn on it.

Read every image listed in the batch file, one at a time, in order. Then emit
one row per image.

What the red rectangles mean, and this is all the context you need:

- Each rectangle marks a region that is cut out of the page **at its own,
  higher resolution** and handed separately to a vision model. Nothing outside
  any rectangle is ever looked at as an image.
- We are considering replacing all of those separate cut-outs with **one
  image: the whole page, at exactly the size and sharpness of the PNG you are
  looking at**. The PNG is not a preview; it is the replacement.
- The page's running text, headings, captions and any ruled table are
  recovered separately as plain text, so text and tables outside the
  rectangles are **not** a loss.
- So the questions are only about **graphics**: charts, plots, diagrams,
  schematics, circuit drawings, waveforms, photographs, micrographs, maps,
  timing diagrams, illustrations — anything whose meaning requires seeing it.

Answer **two** questions per image.

**Q1 — `outside`.** Is there a graphic, as defined above, at least partly
outside every red rectangle, whose content is not also present inside one of
the rectangles?

- `yes` — there is such a graphic.
- `no` — everything outside the rectangles is text, tables, headings,
  equations, page furniture, logos, vendor marks, rules, borders, or graphics
  that merely repeat what is already inside a rectangle.

**Q2 — `detail`.** Look only *inside* the red rectangles, in the PNG in front
of you. Is everything in them still readable at this size — axis numbers, tick
labels, pin names, part designators, legend entries, curve separations, fine
hatching, small annotations?

- `legible` — yes. Nothing inside the rectangles needs more magnification than
  this image gives you.
- `lost` — no. At least one rectangle contains detail you cannot resolve here:
  text too small to read, curves that merge, a schematic whose connections you
  cannot trace.

Rules for the hard cases:

- Small icons, company logos, header/footer rules and page decorations are
  **not** graphics for Q1. Answer `no`.
- Mathematical display equations, however elaborate, are **not** graphics.
- If the same figure straddles a rectangle's edge — the rectangle clips a
  panel of one figure — that is `yes` for Q1, because part of the graphic is
  unseen.
- For Q2, judge only what is inside the rectangles. Text elsewhere on the page
  being unreadable is irrelevant.
- **Break every tie against the change.** If you are unsure whether something
  outside the rectangles is real graphic content or decoration, answer `no` to
  Q1. If you are unsure whether something inside a rectangle is readable,
  answer `lost` to Q2.
- If you cannot find any red rectangle on the page at all, write `norect` in
  both columns.

Output a TSV file at the path you are given, with exactly this header:

    tag	outside	detail	note

One row per image, in batch order. `note` is a short phrase, at most twelve
words: name what is outside the rectangles, or what is unreadable inside them.
Write nothing else into the file.
