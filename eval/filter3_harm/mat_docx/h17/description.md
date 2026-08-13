One figure on this page (Figure 3), a two-panel chart with a shared legend. The rest of the page (body prose, Table 5, Table 6, footnote) is extractable text and is not reproduced here.

Caption below the figure: "Figure 3: **Left:** runtime of forward pass + backward pass. **Right:** attention memory usage."

Shared legend, six series (two rows of three), line style is the encoding:

- FlashAttention — black dotted
- PyTorch Attention — blue solid
- Linformer Attention — brown solid
- Block-Sparse FlashAttention — green dashed
- Megatron Attention — orange solid
- OpenAI Sparse Attention — pale-teal dashed

## Figure 3, left panel — line chart, "Attention Runtime (Fwd Pass + Bwd Pass)"

- **X axis:** "Sequence Length", log-spaced tick labels 128, 256, 512, 1024, 2048, 4096, 8192.
- **Y axis:** "Runtime (ms)", logarithmic, decade labels 10⁰, 10¹, 10². Plot area extends slightly below 10⁰ (bottom edge ≈0.35) and slightly above 10².
- **Annotation:** "Crossover Points" in black, with a red leader that forks to two small red open circles drawn on the plot. Circle 1 sits at roughly x ≈ 768, y ≈ 1.6 ms (read from axis); circle 2 sits at roughly x ≈ 4096, y ≈ 35 ms (read from axis).

Values read from the axis (all approximate, log scale):

| Series | Value at 128 | Value at 256 | Value at right-hand end |
|---|---|---|---|
| FlashAttention (black dotted) | ~0.42 ms | ~0.42 ms | ~130 ms at 8192 |
| Block-Sparse FlashAttention (green dashed) | ~0.38 ms | ~0.38 ms | ~7 ms at 8192 |
| Linformer Attention (brown) | ~1.5 ms | ~1.5 ms (flat out to ~1024) | ~15 ms at 8192 |
| OpenAI Sparse Attention (teal dashed) | ~2.4 ms | ~2.2 ms (shallow dip to ~512) | ~35 ms at 4096 — series ends there |
| PyTorch Attention (blue) | ~0.85 ms | ~0.85 ms | ~120 ms at 4096 — series ends there |
| Megatron Attention (orange) | ~0.85 ms | ~0.85 ms | ~17 ms at 2048 — series ends there |

Absences that carry meaning: PyTorch Attention stops at 4096, Megatron Attention stops at 2048, and OpenAI Sparse Attention stops at 4096; only FlashAttention, Block-Sparse FlashAttention and Linformer are plotted all the way to 8192.

## Figure 3, right panel — line chart, "Attention Memory Usage"

- **X axis:** "Sequence Length", tick labels 256, 8K, 16K, 32K, 64K (the 256 tick is at the left edge; spacing between 8K…64K is linear).
- **Y axis:** "Memory Footprint (GB)", linear, labelled ticks at 10 and 20 only; plot top ≈26 GB, bottom at 0.
- **Annotations:** "20x" with a downward black arrow near the left of the plot (arrow spans from roughly 10 GB down to ~3 GB, read from axis); "2x" with a downward black arrow at the far right near 64K (spanning from roughly 22 GB down to ~14 GB, read from axis).

Values read from the axis:

| Series | Behaviour |
|---|---|
| Linformer Attention (brown) | Straight line from ~0 at 256 to ~26 GB at 64K (read from axis) |
| FlashAttention (black dotted) and Block-Sparse FlashAttention (green dashed) | Overlaid on one another; straight line from ~0 at 256 to ~13 GB at 64K (read from axis) |
| PyTorch Attention (blue) | Very steep short segment, reaching ~17 GB at roughly 4K sequence length, then ends |
| Megatron Attention (orange) | Very steep short segment, reaching ~5 GB near the left edge, then ends |
| OpenAI Sparse Attention (teal dashed) | Very short segment, ~3 GB near the left edge, then ends |

Absence that carries meaning: PyTorch, Megatron and OpenAI Sparse Attention all terminate within the first few thousand tokens (out of memory); only Linformer and the two FlashAttention variants extend to 64K.

Page furniture: page number 9.
