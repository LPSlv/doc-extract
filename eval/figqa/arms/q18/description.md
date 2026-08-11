**Page render (`p003-render.png`).** A single-page, two-column physics preprint page. At the top, spanning both columns, is **TABLE II** — a four-panel quantum-circuit figure with a rule above and below the panel headers — followed by its caption and then two columns of body text.

---

### TABLE II — circuit diagram (top of page)

The table has four column headings, separated by horizontal rules above and below the heading row:

| *Z* Plaquette | (Static) surface code | Walking surface code | Moonwalking surface code |

**Panel 1 — *Z* Plaquette (leftmost).** A blue-shaded quadrilateral (a leaning trapezoid) with filled black dots at its corners and one in its interior. Vertex labels, and the horizontal wire stubs leading right from each dot into the circuits, are, top to bottom: **1** (top-right vertex), **2** (upper-left vertex), **a** (the interior dot, the ancilla, with its label set above and to the left of the dot), **3** (lower-right vertex), **4** (bottom-left vertex). So the five circuit wires, top to bottom, are qubit 1, qubit 2, ancilla *a*, qubit 3, qubit 4.

All three circuit panels use the same five wires in that order, and each has four vertical **dashed blue lines** marking time slices, labelled at the top **A**, **B**, **C**, **D** (left to right). Gates are drawn as boxes (**rz**, **mz**, **mx**) and as CX/CNOT symbols (filled dot = control, ⊕ = target, joined by a vertical line).

**Panel 2 — (Static) surface code.** Every wire starts with no box except the ancilla wire, which begins with an **rz** box. Then, left to right:

1. A violet, dotted SWAP gate drawn as two violet **×** markers, one on the qubit-1 wire and one on the ancilla wire, joined by a violet dotted vertical line and labelled **L** (label sits between the two markers). This is before time slice A.
2. CX with control on **qubit 1**, target ⊕ on the **ancilla** — before slice A.
3. Dashed line **A**.
4. CX with control on **qubit 2**, target ⊕ on the **ancilla** — between A and B.
5. Dashed line **B**.
6. CX with control on **qubit 3**, target ⊕ on the **ancilla** — between B and C.
7. Dashed line **C**.
8. CX with control on **qubit 4**, target ⊕ on the **ancilla** — between C and D.
9. Dashed line **D**.
10. An **mz** box terminating the **ancilla** wire.

No measurement box appears on any data wire (1, 2, 3, 4) in this panel; only the ancilla is measured.

**Panel 3 — Walking surface code.** No leakage-SWAP marker. The ancilla wire begins with an **rz** box. Then, left to right:

1. CX with control on **qubit 1**, target ⊕ on the **ancilla** — before slice A.
2. Dashed line **A**.
3. CX with control on **qubit 2**, target ⊕ on the **ancilla** — between A and B.
4. Dashed line **B**.
5. CX with control on **qubit 3**, target ⊕ on the **ancilla** — between B and C.
6. Dashed line **C**.
7. CX with control on the **ancilla** and target ⊕ on **qubit 4** (direction reversed relative to the earlier gates) — between C and D.
8. Dashed line **D**.
9. Measurements at the right-hand end: **mz** on qubit 1, **mx** on qubit 2, **mx** on qubit 3, **mz** on qubit 4. The ancilla wire ends bare, with no measurement box.

**Panel 4 — Moonwalking surface code.** No leakage-SWAP marker. The ancilla wire begins with an **rz** box. Then, left to right:

1. CX with control on **qubit 1**, target ⊕ on the **ancilla** — before slice A.
2. Dashed line **A**.
3. CX with control on **qubit 3**, target ⊕ on the **ancilla** — between A and B. (Note the ordering: qubit 3 is used here, before qubit 2.)
4. Dashed line **B**.
5. CX with control on **qubit 2**, target ⊕ on the **ancilla** — between B and C.
6. Dashed line **C**.
7. CX with control on the **ancilla** and target ⊕ on **qubit 4** — between C and D.
8. Dashed line **D**.
9. Measurements at the right-hand end: **mz** on qubit 1, **mx** on qubit 2, **mx** on qubit 3, **mz** on qubit 4. The ancilla wire ends bare.

So the CX ordering onto the ancilla is 1, 2, 3, 4 for the static and walking circuits and 1, 3, 2, 4 for the moonwalking circuit; the walking and moonwalking circuits both end with an ancilla-controlled CX onto qubit 4 and measure the four data qubits rather than the ancilla.

**Caption:**

> TABLE II: One round of *Z*-stabilizer measurement for each of the three circuits analyzed (Sec. III A), with markers we will use to define the four erasure check (EC) schedules (Sec. III B). The `rz` gate resets the qubit into the |0⟩ state. The `mz` and `mx` gates measure the qubit in the *Z* and *X* basis, respectively. For the static surface code, the ancilla (qubit *a*) measurement result gives the *Z* stabilizer value, while for the walking and moonwalking circuits, the stabilizer is measured by qubit 4. The violet, dotted SWAP gate labeled "L" indicates a leakage-SWAP gate which leaves the computational-basis states untouched; it is only used for EC schedule 8 in the static surface code circuit. For EC schedule 8 in all circuits, every measurement is replaced by three-state measurement. The remaining EC schedules use mid-circuit erasure checks: EC schedule 4 has erasure checks on all qubits at time slice D; EC schedule 2 has erasure checks at time slices B and D; and EC schedule 1 has erasure checks at all time slices A, B, C, and D. When a mid-circuit erasure check is followed immediately by a measurement, they may be combined into a three-state measurement.

---

### Body text, left column

[32], transferring leakage from data to ancilla qubits and resetting any leaked data qubits to the qubit subspace. Where leakage-SWAP gates are used (see Sec. III A), they are considered noiseless.

**III. CIRCUIT DESIGN SPACE**

In this section we introduce the moonwalking surface code, which we will compare to the conventional static and walking surface code implementations in terms of their performance against leakage and erasure errors in Sec. V. Leakage-to-erasure conversion is integrated into all three circuits using mid-circuit erasure checks and/or three-state measurements, plus leakage-SWAP gates when necessary.

**A. Syndrome extraction circuits**

The static, walking, and moonwalking surface code circuits differ in their syndrome extraction circuits as seen from the *Z* stabilizer measurement circuit snippets shown in Table II.

The static surface code uses the standard circuit in which CX gates are applied between an ancilla initialized in |0⟩ (|+⟩) and the data qubits of a *Z* (*X*) plaquette and then the ancilla is measured in the *Z* (*X*) basis. As will be discussed in Sec. III B, we cannot convert every qubit's leakage into erasure in the static surface code circuit without mid-circuit erasure checks or leakage-SWAP gates. For this reason, we are interested in dynamic circuits which reassign data and ancilla qubits every syn-

### Body text, right column

drome extraction cycle. This reassignment means every qubit is regularly measured and reset, enabling erasure conversion with only three-state measurement.

The specific dynamic circuits we study are the walking surface code, introduced in Ref. [34], and the proposed moonwalking surface code. Remarkably, we find that even though the moonwalking circuit is simply the time-reversed walking circuit, it has significantly improved scaling when using infrequent erasure checks under skip-gate leakage. We note that the existence of a time-reversed walking circuit was mentioned in Ref. [34] but its unique properties, particularly regarding different leakage noise effects and including erasure conversion, were not studied.

The walking and moonwalking surface code circuits can each be constructed from the static surface code circuit by inserting a pair of SWAP operations. For the moonwalking circuit, the SWAPs are inserted between the reset and the first CX, as shown in Fig. 2. For the walking circuit, the SWAPs are inserted between the last CX and the measurement, as shown in Fig. 6. One of the SWAPs is commuted through the reset (measurement) for the moonwalking (walking) circuit. In the context of the code, the effect of the SWAP between syndrome extraction rounds is trivial as it can be recovered by shifting the data qubits diagonally by half a plaquette in software so that they appear to be placed on the ancilla qubit sublattice of the previous round. Indeed, the simple removal of the SWAP still gives a good syndrome extraction circuit. These circuits move the logical patch one step diagonally. By spatially rotating the circuit for the next round of syndrome extraction, the patch is stepped diagonally back to its original position. To finish constructing

---

Page furniture: page number **3**, top right corner. Cross-reference numbers rendered in colour (red for internal section/table/figure references such as "Sec. III A", "Table II", "Fig. 2", "Fig. 6"; blue for citation numbers such as [32] and [34]).
