---
title: A light worker's decode line at a high sample rate rests on two Linux readings, and the Mac measured the analysis line at twice Linux's
found: while building #728, U275, 2026-11-12.
issue: no
---

**The mechanism.** `analysis/light.py` costs a light worker at the larger of
two lines over a base. U275 raised the analysis line and the base to what six
CD quality library tracks peaked at on the Mac, 2.76 MB a second through
their ends, where Linux had measured 1.35. The decode line, four bytes a
sample frame for each channel plus three more channels' worth, is unchanged:
it rests on two Linux readings of one eleven minute file stored at 192
kilohertz, 2054 and 2180 MB. If the decode on the Mac grows by the same
factor the analysis did, a 192 kilohertz file there would peak near 4 GB
against the 2801 MB it is now declared at. At 96 kilohertz the decode is now
under the analysis line and the Mac's analysis figure covers it.

**Measured cost.** None observed; not driven, since the container holds no
Mac. A high rate file on the Mac could be declared under its peak, so the
planner could afford a worker the machine cannot carry, which the headroom
(half of what is available on darwin), the reserve and the pressure gates
stand behind. A folder of CD quality tracks, the case A121 measured, is
covered.

**Closes when:** `scripts/analyze_stages.py memory` is run on the Mac over at
least one 96 or 192 kilohertz file and the decode constants are confirmed or
raised from its reading. Ledger only.
