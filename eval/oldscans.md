# olmOCR-bench old_scans — where the visual layer wins

Corpus: https://huggingface.co/datasets/allenai/olmOCR-bench
(`old_scans` 98 + `old_scans_math` 36 = 134 PDFs, 984 unit tests, ODC-BY).

Every sampled file classifies `scanned`, reports `pages_needing_ocr=[1]`, and
yields **zero** extractable characters. pdf-inspector alone therefore scores ~0;
the render-and-read path is the entire value.

Confirmed end to end on a handwritten 1914 letter (cursive, which Tesseract also
fails): rendered at 140 dpi and transcribed in full.

## Procedure

1. Download `bench_data/pdfs/old_scans*`.
2. Run the full pipeline; `no_text_layer` pages route to transcription.
3. Score with olmOCR-bench's unit tests (text presence, absence, reading order,
   table accuracy).

Report the number against a text-only baseline of ~0. This is the only official
benchmark that measures what this skill adds.
