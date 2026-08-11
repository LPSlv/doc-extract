**Figure (three-panel system/flow diagram with clip-art icons, p3).** A left-to-right pipeline for multi-objective reinforcement learning from human preferences, split into three bordered boxes of unequal width: a narrow left panel, a wide central panel, and a narrow right panel. No axes, no numeric data, no legend.

---

**Left panel — "Unsupervised Pre-Training".** Title text at the top of the panel: **"Unsupervised Pre-Training"** (two lines). Below it, three purple robot clip-art figures: one at the top with both arms raised, one at the lower left crouching, and one at the lower right beside a small multi-coloured cube (a block/toy object). Caption at the bottom of the panel, two lines: **"Maximize H(s)"** / **"for Multiple Objectives"**.

---

**Central panel — reward learning and policy learning loop.** Contents, roughly left to right:

- **Environment**: an Earth/globe icon at the top left.
- **Policy**: a purple robot icon below the globe, labelled **π_φ** underneath it. Two curved dashed arrows form a loop between the robot and the globe (one arrow up on the left, one arrow down on the right) — the agent–environment interaction cycle.
- A solid arrow leaves the globe to the right, annotated with the transition tuple **(s, a, s′)** in bold. It splits into two branches feeding the two reward models.
- **Reward Model I** — a blue trapezoid, text inside on three lines: **"Reward Model I"** and **r̂_ψ₁** (hat r subscript psi-one, bold).
- **Reward Model II** — a yellow/orange trapezoid below it, text inside: **"Reward Model II"** and **r̂_ψ₂**.
- Each reward model's output arrow is annotated: **r̂_ψ₁(s, a)** from Model I and **r̂_ψ₂(s, a)** from Model II. Both arrows converge and feed a single arrow into the buffer.
- **Shared Replay Buffer** — an orange cylinder (database symbol) in the middle right, labelled on three lines: **"Shared Replay Buffer"**.
- **Preference queries (two of them).** Above the buffer and below it sit two white query panels, each a pair of side-by-side framed thumbnails showing a robot clip-art performing a behaviour, each pair headed by a **green check mark ✓** over the left thumbnail and a **red cross ✗** over the right thumbnail — a two-alternative preference choice.
  - *Upper pair*: robot reaching toward a target/dartboard with a red flag; a curved dashed motion arrow in each thumbnail (curving toward the target on the left, away on the right).
  - *Lower pair*: the same robot-and-target scene but with an added orange object (a stack/pile item) on the right of each thumbnail.
- **Human annotators**: a blue-shirted person icon to the right of the upper query pair, and a yellow/orange-shirted person icon to the right of the lower query pair — one human per reward model, colour-matched to the trapezoid colours (blue → Reward Model I, yellow → Reward Model II).
- **"Reward Learning"** — label on the arrow at the very top of the panel; a black arrow runs from the upper query pair back left and down into the top edge of Reward Model I. The symmetric arrow from the lower query pair runs left and up into the bottom edge of Reward Model II.
- Black arrows also run from the Shared Replay Buffer up into the upper query pair and down into the lower query pair.
- **"Multi-Objective Policy Learning"** — label on the long arrow along the bottom of the panel, which runs from the right side of the Shared Replay Buffer leftward and then up into **π_φ** (the policy robot), closing the loop.

---

**Right panel — "Multi-Objective Policy Learning".** A purple robot icon in the centre with a blue-shirted person above-right of it and a yellow/orange-shirted person below-right of it (the same two annotator colours as the central panel). A curved dashed arrow arcs over the robot toward the upper right, labelled **π_φ**. Caption at the bottom of the panel, two lines: **"Multi-Objective Policy Learning"**.

---

All symbols appearing in the graphic: (s, a, s′), r̂_ψ₁, r̂_ψ₂, r̂_ψ₁(s, a), r̂_ψ₂(s, a), π_φ, H(s), ✓, ✗. No part numbers, dates or other printed numerals appear.
