**Figure 5.1 (p118, EFM32GG11 Family Data Sheet, §5.1) — "EFM32GG11B8xx in BGA192 Device Pinout".**

**Type:** package ball-map / pinout drawing (top-side view of a 192-ball BGA). A plain rectangular package outline; a solid grey dot just inside the top-left corner is called out by a leader line labelled "Pin A1 index". Column numbers 1–16 run left to right along the top edge; row letters run down the left edge: A, B, C, D, E, F, G, H, J, K, L, M, N, P, R, T (the ambiguous letters I, O, Q and S are skipped). Each ball is a small circle carrying its signal name in text rotated about 45°.

Population: rows A, B, C, P, R and T are fully populated across columns 1–16; rows D, E, M and N carry balls only in columns 1–3 and 14–16; rows F, G, H, J, K and L carry balls in columns 1–3, 6–11 and 14–16. Columns 4, 5, 12 and 13 are empty in the middle rows, and the middle of the package (columns 6–11 of rows F–L) is a power/ground island of IOVDD/VSS balls. 16 + 16 + 16 + 6 + 6 + 12 + 12 + 12 + 12 + 12 + 12 + 6 + 6 + 16 + 16 + 16 = 192 balls.

**Legibility note:** the ball labels are rendered at roughly 3 px of text height and are set at 45°. The port letters are reliable; single digits are at the limit of resolution. Entries below marked "(?)" are the most likely reading but the digit could not be confirmed; entries marked "illegible" could not be read at all.

**Ball map as read (row: column = signal):**

| Row | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | PA15 | PE15 | PE14 | PE13 | PE12 | PE11 | PE10 | PE9 | PE8 | PI9 | PI6 | PF14 | VBUS | PF11 | PF10 | PF9 (?) |
| B | PA0 | PD11 | PD10 | PD9 | PF9 (?) | PF8 | PF7 | PF6 | PI11 (?) | PI5 (?) | PF5 | PF13 | PF3 | PF2 | PF1 | VREGO |
| C | PA1 | PD12 | PD14 (?) | PD13 | PI15 | PI14 | PI13 | PI12 | PI10 (?) | PI7 | PF15 | PF12 | PF4 | PC15 | PC14 | VREGI |
| D | PA2 | PG0 | PD15 | – | – | – | – | – | – | – | – | – | – | PC13 | PC12 | PC11 |
| E | PA3 | PG2 | PG1 | – | – | – | – | – | – | – | – | – | – | PC10 | PC9 | PC8 |
| F | PA4 | PG4 | PG3 | – | – | IOVDD2 | IOVDD1 | VSS | NC | IOVDD0 | IOVDD0 | – | – | PI5 (?) | PI4 | PI3 |
| G | PA5 | PG6 | PG5 | – | – | IOVDD2 | IOVDD1 | VSS | VSS | IOVDD0 | IOVDD0 | – | – | PI2 | PI1 | PI0 |
| H | PA6 (?) | PG8 | PG7 | – | – | VSS | VSS | VSS | VSS | VSS | VSS | – | – | PE5 | PE6 | PE7 |
| J | PG11 | PG10 | PG9 | – | – | VSS | VSS | VSS | VSS | VSS | VSS | – | – | PE3 | PE4 | DECOUPLE |
| K | PG14 | PG13 | PG12 | – | – | IOVDD0 (?) | IOVDD0 (?) | VSS | VSS | IOVDD[digit illegible] | IOVDD[digit illegible] | – | – | PE1 | PE2 | DVDD |
| L | PG15 | PB15 (?) | PB0 (?) | – | – | IOVDD0 (?) | IOVDD0 (?) | VSS | VSS | IOVDD[digit illegible] | IOVDD[digit illegible] | – | – | PE0 | PC7 | VREGVDD |
| M | PB1 | PB2 | PB3 | – | – | – | – | – | – | – | – | – | – | PC6 (?) | VREGVSS | VREGSW |
| N | PB4 | PB5 | PB6 | – | – | – | – | – | – | – | – | – | – | PD5 | PD4 | VREGVSS |
| P | PC0 | PC1 | PC2 | PA8 (?) | PA11 | PA13 | PB9 | PB12 (?) | PH2 | PH5 | PH6 (?) | PH11 (?) | PH13 | PD0 | PD3 | PD8 (?) |
| R | PB7 | PC3 | PC5 | PA9 (?) | BOOTEN (?) | RESETn | PB10 (?) | PH0 | PH3 | PH6 (?) | PH8 | PH12 | PH14 | PH15 | PD2 | PD7 |
| T | PB8 | PC4 | PA7 | PA10 | PA12 | PA14 | PB11 | PH1 | PH4 | PH7 | PH10 | PB13 | PB14 | AVDD (?) | PD1 | PD6 |

("–" = no ball at that position.)

Named non-GPIO balls that are legible in the map: VBUS (A13), VREGO (B16), VREGI (C16), DECOUPLE (J16), DVDD (K16), VREGVDD (L16), VREGVSS (M15 and N16), VREGSW (M16), RESETn (R6), the large VSS / IOVDD0 / IOVDD1 / IOVDD2 island in the package centre, and one NC ball at F9.

The rest of the page is running text and Table 5.1 ("EFM32GG11B8xx in BGA192 Device Pinout", columns Pin Name / Pin(s) / Description), which are ordinary extractable text.

Page furniture: header "EFM32GG11 Family Data Sheet" / "Pin Definitions"; footer "silabs.com | Building a more connected world.", "Rev. 1.2 | 118".
