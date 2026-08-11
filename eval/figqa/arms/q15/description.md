**Figure 13 (page render, `p022-render.png`).** A three-row composite figure. Each row is one real-world manipulation task and contains four elements: a green-tinted filmstrip of five frames captioned as a success, a line chart of the value curve for that successful trajectory, a second filmstrip on the right split into coloured phase groups, and a second line chart for the failed trajectory with vertical coloured bands matching those phase groups. The robot in every frame is a black robot arm viewed side-on against a grey tabletop.

Both charts in every row use the same axis convention: Y axis titled **Value**, X axis titled **Steps**. Curves are single thin grey/black lines, unlabelled apart from the axes.

---

**(a) Conveyor Belt Sushi Picking** — sub-caption printed below the row.

*Left (success), filmstrip:* five frames of the arm above a rotating belt with a small orange/white sushi item; green rounded panel captioned **"Successfully picking the Chutoro Nigiri from the rotating belt."**

*Left chart:* Y axis ticks **−0.5, −0.6, −0.7, −0.8, −0.9, −1.0** (top to bottom). X axis ticks **10, 20, 30, 40, 50, 60**. The curve starts near −0.87 at about step 6, stays flat to roughly step 18, then rises in steps — about −0.83 at step 22, a plateau near −0.78 around steps 27–32, a brief dip near step 33, then a steep rise between steps 34 and 42 to about −0.60, after which it is flat at roughly −0.59 to −0.60 out to step 63.

*Right (failure), filmstrip:* three coloured groups, left to right — a green panel with one frame captioned **"Reaching."**; a yellow panel with two frames captioned **"Waiting for too long."**; a red/pink panel with two frames captioned **"Missing."**

*Right chart:* Y axis ticks **−0.5, −0.6, −0.7, −0.8, −0.9, −1.0**. X axis ticks **10, 20, 30, 40, 50, 60, 70, 80**. Three shaded vertical bands: green spanning roughly steps 13–28, pale yellow roughly steps 30–41, pink roughly steps 50–74. The curve starts near −0.85 at step 5, dips to about −0.90 near step 8, rises through the green band to about −0.76 near step 22, sags to about −0.82 through the yellow band, rises again to a local maximum of about −0.70 near step 47, then declines irregularly across the pink band and drops sharply after step 76 to about −0.93 at step 80.

---

**(b) Cloth Folding** — sub-caption printed below the row.

*Left (success), filmstrip:* five frames of the arm manipulating a red cloth; green panel captioned **"Successfully folding the cloth."**

*Left chart:* Y axis ticks **1.01, 0.63, 0.24, −0.14, −0.52** (top to bottom). X axis ticks **0, 50, 100, 150, 200, 250, 300, 350, 400**. The curve rises almost monotonically from about −0.52 at step 0 to about **1.0** at step ~390, with small oscillations; notable features are a small dip near step 140 (down to roughly −0.15 from a local peak near −0.05), a steeper climb between steps 150 and 200, and a further steady climb from about 0.35 at step 200 to about 1.0 at step 390.

*Right (failure), filmstrip:* green panel, one frame, **"Reaching."**; yellow panel, two frames, **"Grasping but slipping."**; pink panel, two frames, **"Not folded properly."**

*Right chart:* Y axis ticks **1.0, 0.5, 0.0, −0.5, −1.0**. X axis ticks **0, 50, 100, 150, 200, 250, 300**. Shaded bands: green roughly steps 0–50, pale yellow roughly steps 78–130, pink roughly steps 133–300 (extending to the right edge). The curve starts near −0.95 at step 0, climbs through the green band to about 0.4 near step 48, drops to about −0.35 near step 60, spikes to roughly 0.65 near step 80 inside the yellow band, oscillates down to about −0.75 near step 130, then fluctuates through the pink band mostly between −0.7 and +0.5 with a peak near 0.6 around step 170 and another near 0.5 around step 230, ending near −0.5 at step ~295.

---

**(c) Stovetop Cleaning** — sub-caption printed below the row.

*Left (success), filmstrip:* five frames of the arm over a white surface with small dark debris, a large red dot (button) and a blue/yellow object at the rear; green panel captioned **"Successfully cleaning the stovetop and pushing the button."**

*Left chart:* Y axis ticks **1.04, 0.86, 0.69, 0.51, 0.34** (top to bottom). X axis ticks **0, 50, 100, 150, 200, 250**. The curve rises steadily and noisily from about 0.35 at step 0 to about 1.03 near step 260, roughly linear with small oscillations throughout; approximate intermediate values 0.50 at step 50, 0.63 at step 100, 0.78 at step 150, 0.90 at step 200.

*Right (failure), filmstrip:* four separate panels, left to right — green **"Grasping."**, pink **"Falling."**, green **"Reaching."**, pink **"Missing."**

*Right chart:* Y axis ticks **0.21, 0.09, −0.02, −0.14, −0.26** (top to bottom). X axis ticks **0, 50, 100, 150, 200, 250**. Shaded bands: a narrow green band roughly steps 3–16, a pink band roughly steps 16–65, a green band roughly steps 70–96, then a wide pink band from roughly step 96 to the right edge (~250). The curve starts near −0.25 at step 0, jumps to about 0.09 by step 18, holds near 0.05–0.08 to step 40, falls to about −0.24 near step 63, rises steeply through the second green band to a maximum of about **0.21** near step 95, then oscillates for the rest of the trace mostly between −0.15 and +0.10, with a deep dip to about −0.17 near step 190, ending near 0.09 at step ~248.

---

**Caption (printed beneath the figure):**

> **Figure 13** WCM value curve in the real world. Unlike simulation, real-world trajectories are not ideal: teleoperated trajectories are subject to various confounding factors, and both the environment and the camera introduce visual noise. Consequently, even successful trajectories show certain fluctuations. Nevertheless, the discriminability between successful and failed trajectories remains high.

All curve values above that are not printed on the image are read off the axes and are approximate.

Page furniture: page number 22, centred at the foot of the page.
