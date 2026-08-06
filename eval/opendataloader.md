# opendataloader-bench — regression gate

Corpus: https://github.com/opendataloader-project/opendataloader-bench
(200 PDFs, Apache-2.0, official NID/TEDS/MHS evaluators in `src/`).

## Procedure

1. Register an engine in `src/engine_registry.py` plus a `pdf_parser_*.py` that
   runs the full doc-extract pipeline.
2. **Strip** delimited blocks from the output (`artifact.strip`) before writing
   the prediction.
3. Assert the stripped prediction is byte-identical to raw
   `pdf_inspector.process_pdf(path).markdown`.
4. `uv run src/evaluator.py --engine doc-extract`.

## Gate

| Metric | Minimum |
|---|---|
| Overall | 0.875 |
| Reading order | 0.915 |
| Tables | 0.814 |

Equal, not better. Measured headroom on this corpus is ~zero: pdf-inspector
already extracts a table in 40 of the 42 documents that have one, and its table
score is limited by TEDS structure error and 11 spurious tables, neither of
which a visual layer can address. The gate exists to prove no regression.

## Observed routing (harvest.py, engine 0.2.6)

    200 docs · 0 errors · 105 touched · 132 vision calls
    standalone_raster 107 · curves 16 · dense_grid 7 · stroke_grid 1 · no_text_layer 1
