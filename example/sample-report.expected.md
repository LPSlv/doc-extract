# Sample Project Report

## Work package 3 - quarterly summary

This is a synthetic document used as the runnable example for the doc-extract skill. It contains ordinary body text, a table that a text extractor can parse on its own, and a chart that it cannot. Running the skill over it should extract all the text, skip the table (already handled), and send exactly one image to a vision pass.

### Budget by category

|Category|Planned|Actual|
|---|---|---|
|Personnel|48,000|45,200|
|Equipment|22,000|24,800|
|Travel|6,000|3,100|
|Total|76,000|73,100|

***Figure 1: spend against plan***

Actual spend tracked plan closely through Q2 but diverged in Q3 as equipment procurement slipped. The variance is expected to close in Q1 of the following year.

<!-- doc-extract:add -->
## Figures and scanned pages

**[p1] p001-x38** (standalone_raster) — Line chart, two series, spend against plan. X: Quarter 2026 (Q1-Q4). Y: Spend (k EUR), 10 to just over 31. Planned (blue, circles): Q1 12, Q2 19, Q3 24, Q4 31. Actual (orange, squares): Q1 11, Q2 17, Q3 18, Q4 22. The two series track closely at Q1-Q2 then diverge from Q3 onward, with Actual flattening while Planned continues to rise; the Q4 gap is about 9k EUR.
<!-- /doc-extract:add -->
