**Figure (two-panel flow diagram, p4).** Side-by-side comparison of the existing "ORSF Algorithm" (left panel, solid rounded border) and the "Proposed ORSF Algorithm" (right panel, dashed rounded border). Both panels have an identical top block, an identical bottom block, and differ only in the two decision diamonds in the middle and the resulting equations.

Panel titles sit in yellow rounded boxes at the top of each panel: **"ORSF Algorithm"** (left), **"Proposed ORSF Algorithm"** (right).

**Top block (identical in both panels).** A white rounded box holding a bracketed data matrix. Column headers, italic: `x1  x2  x3  x4  x5  δ  T`. Row labels down the left, bold: `1, 2, 3, ⋮, n`. Matrix entries:

| row | x1 | x2 | x3 | x4 | x5 | δ | T |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 45 | 130 | 5.5 | 1 | 1 | 7 |
| 2 | 0 | 30 | 125 | 2.3 | 0 | 0 | 3.5 |
| 3 | 1 | 50 | 120 | 4.5 | 0 | 1 | 10 |
| ⋮ | ⋮ | ⋮ | ⋮ | ⋮ | ⋮ | ⋮ | ⋮ |
| n | 0 | 65 | 110 | 4.9 | 1 | 0 | 12 |

Beneath the matrix, inside the same white box, a pink rounded pill labelled **"Non-leave Node Data"**.

**Middle (the difference).** From the "Non-leave Node Data" pill a single solid line drops and forks left and right into two solid arrows, each terminating on a decision diamond.

- Left panel, diamonds are white/unfilled:
  - left diamond: **"fast, Cox PH"**
  - right diamond: **"Net"** with smaller text below inside the diamond: *"(user pre-define # of variables, e.g., 3)"*
- Right panel, diamonds are blue-filled:
  - left diamond: **"LASSO"**
  - right diamond: **"MRMR, CARS"** (two lines)

From each diamond a **dashed** arrow points down into the bottom block.

**Bottom block (green rounded box, both panels).** Caption at the bottom of the box in both panels: **"Linear Combinations of Input Variables (LCIVs)"**. Inside each green box are two white equation boxes, one under each diamond.

Left panel equations:

$$\eta = \beta_1 x_1 + \beta_2 x_2 + \beta_3 x_3 + \beta_4 x_4 + \beta_5 x_5$$

$$\eta = \beta_2 x_2 + \beta_4 x_4 + \beta_5 x_5$$

Right panel equations:

$$\eta = \beta_3 x_3 + \beta_5 x_5$$

$$\eta = \beta_1 x_1 + \beta_2 x_2 + \beta_5 x_5$$

So the left ("fast, Cox PH") branch keeps all five variables, the left panel's "Net" branch keeps three (x2, x4, x5), the proposed "LASSO" branch keeps two (x3, x5), and the proposed "MRMR, CARS" branch keeps three (x1, x2, x5).

No axes, numbers, or units other than the matrix values; no legend; no figure caption inside the image.
