# The labelling instruction, verbatim

Every labeller was given exactly this text plus one batch file, and nothing
else — no file names, no corpus, no page numbers, no statement of what the
answer would be used for and no indication of which answer is convenient.

---

You are labelling page images. Each PNG is one page of a PDF document,
rendered whole. A red rectangle is drawn somewhere on it.

Read every image listed in the batch file, one at a time, in order. Then emit
one row per image.

What the red rectangle means, and this is all the context you need:

- The rectangle marks the only region of the page that is cut out and handed
  to a vision model. Nothing outside the rectangle is ever looked at as an
  image.
- The page's running text, headings, captions and any ruled table are
  recovered separately as plain text, so text and tables outside the rectangle
  are **not** a loss.
- So the question is only about **graphics**: charts, plots, diagrams,
  schematics, circuit drawings, waveforms, photographs, micrographs, maps,
  timing diagrams, illustrations — anything whose meaning requires seeing it.

Label each page with exactly one of:

- `loses` — there is a graphic, as defined above, at least partly **outside**
  the red rectangle, whose content is not also present inside the rectangle.
- `sufficient` — everything outside the rectangle is text, tables, headings,
  equations, page furniture, logos, vendor marks, rules, borders, or graphics
  that merely repeat what is already inside the rectangle.

Rules for the hard cases:

- Small icons, company logos, header/footer rules and page decorations are
  **not** graphics for this purpose. `sufficient`.
- Mathematical display equations, however elaborate, are **not** graphics.
  `sufficient`.
- If the same figure straddles the rectangle's edge — the rectangle clips a
  panel of one figure — that **is** `loses`, because part of the graphic is
  unseen.
- **Break every tie toward `sufficient`.** If you are unsure whether something
  outside the box is real graphic content or decoration, say `sufficient`.
- If you cannot find a red rectangle on the page at all, label `norect`.

Output a TSV file at the path you are given, with exactly this header:

    tag	label	note

One row per image, in batch order. `note` is a short phrase, at most twelve
words, naming what is outside the rectangle. Write nothing else into the file.
