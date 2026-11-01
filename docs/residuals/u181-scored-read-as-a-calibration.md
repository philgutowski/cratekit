---
title: The upgrade command adds the vocals extra only for a library with a vocal calibration recorded
found: at the plan of #378, U181, 2026-11-01, and confirmed at its review.
issue: no
---

**The mechanism.** The brief asks `install.release` to keep `vocals` when the library has ever scored a track, any file or row carrying a voxlevel. `crate doctor` reads that as a vocal calibration recorded for the library, `_vocals_scored`, since a calibration is fitted only from scored files or set by hand to tag them, and reading every file or row for a voxlevel is not a cost doctor may spend.

**Measured cost.** A library scored and never calibrated gets an upgrade command without `vocals`, in that one state. The `install.extras` row beside it, on a copy that lacks the extra, prints the command with `vocals`, so the report carries the right command. Not driven on a real library.

**Closes when:** a cheap record of a scored track exists to read, for instance the analysis job reports carrying a voxlevel, and the probe reads it. Ledger only.
