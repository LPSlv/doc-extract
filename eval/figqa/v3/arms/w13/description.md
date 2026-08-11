**Figure (two-panel schematic: causal DAG + scatter, and a flow diagram, p2).** Wide two-panel figure with bold lettered panel titles.

**Panel A — "The Simpson trap".** Sub-label in grey below the title: *"(hidden confounder)"*.

- A three-node causal DAG drawn with ellipse nodes. **Z** sits at the top (grey outline); **X** (bottom left) and **Y** (bottom right) sit below it.
- Two **red dashed arrows** run from Z down to X and from Z down to Y.
- One **green solid arrow** runs horizontally from X to Y.
- Below the DAG, in bold green: **"true effect +0.55"**.
- To the right of the DAG, a small scatter plot of dark-red/maroon dots (roughly 80–100 points), forming a clearly downward-sloping cloud from upper left to lower right. It has **no axes, no tick marks, no axis labels and no gridlines**. Its only annotation is the dark-red caption above it: **"obs: corr −0.76"**.
- The panel therefore contrasts a true positive effect (+0.55) against an observational correlation of the opposite sign (−0.76).

**Panel B — "Evidence-type competition at inference (same C1 checkpoint)".** A two-row flow diagram; the two rows share the same model weights and differ only in what evidence is present at inference.

*Top row.* Two colour-keyed labels sit above a light-grey rounded box: **"obs"** in red and **"probes"** in blue. Inside the box, a row of six small squares: **four red squares followed by two blue squares** (4 obs tokens + 2 probe tokens). Directly under the box, in black: **"query: do(X = x) → Y = ?"**. A black arrow runs right from the box to a black-outlined rectangle labelled **"C1 (25M)"**, and a further black arrow runs from that to red bold text reading:

> **obs wins:**
> **slope − ✗ reversed**
> **(19/50 worlds)**

*Transition.* A thick **green downward arrow** drops from the top box to the bottom box, annotated in bold green to its right: **"erase obs at inference (E1b)"**.

*Bottom row.* A single blue label **"probes"** above a second light-grey rounded box containing **four blue squares** and no red squares — the obs tokens are absent. Under the box, the same black line: **"query: do(X = x) → Y = ?"**. A grey arrow runs right, annotated in grey italics above it: *"same weights"*, and terminates at green bold text reading:

> **released:**
> **slope + ✓ correct**
> **(ratio +0.56 ≈ probe-only)**

Colour coding: red = observational evidence / wrong (reversed) outcome; blue = probe evidence; green = correct outcome and the intervention that produces it. A green check mark ✓ marks the correct outcome and a red cross ✗ marks the reversed one.

Numbers appearing anywhere in the graphic: +0.55, −0.76, 25M, 19/50, +0.56, and the square counts 4 red + 2 blue (top) and 4 blue (bottom). No axes, units, legend box or footnote are present.
