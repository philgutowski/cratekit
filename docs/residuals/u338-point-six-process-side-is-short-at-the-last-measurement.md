---
title: U290's point 6 is short at its last measurement, the seventeen scripts at 7,444 lines against 7,374 and the three loaded documents at 1,001 against 975
found: at the build of #987, U338, the last measurement of U290 (#847), 2026-11-25.
issue: no
---

**The mechanism.** Point 6 of #847's definition of done, by U313's and U314's bars as U315 read them: the seventeen scripts the survey counted (`analyze_stages.py`, `board.py`, `calibrate_timing.py`, `ci_deps.py`, `cloud_battery.py`, `cloud_session.sh`, `cyanite_trial.py`, `dump_schemas.py`, `head_agreement.py`, `mutate.py`, `mutate_table.py`, `release.py`, `revendor_downloader.py`, `sample_name_shapes.py`, `scan_repo.py`, `title_differential.py`, `wait_ci.py`) at most 7,374 lines, `board.py` and `mutate.py` each under 1,500; the documents every build thread loads (`docs/METHOD.md`, `CLAUDE.md`, the cloud-unit skill) at most 975; the ledger in files of at most 5,000 lines, searchable. Measured by `wc -l` on `main` at `147574d`:

- the seventeen scripts **7,444**, 70 over. U330 left them at 7,360; U957 (`f9e0a663`, a feature card) added 116 to `scan_repo.py`, U343 took 33 off and U328 added 1.
- `board.py` 1,474 and `mutate.py` 1,191, both under 1,500, so that part holds. `scripts/refactor_measure.py`, outside the seventeen, is 1,591, over the 1,500 that U330's brief also read for every file in `scripts/`: U328 left it at 1,497 and U331 added 94.
- the three documents **1,001** (493, 141, 367), 26 over. U315 read 973 (487, 141, 345); the `merge(method)` of 2026-11-24 (`476696f9`, Phillip's rule that the macOS battery is owed by `main`) added 22 to the skill and 2 to METHOD, and U329, U336 and U331 together 4 to METHOD.
- the ledger: `docs/residual-findings.md` 1,006 lines and twelve archive files of at most 4,997, `board.py residuals --search` naming the archive file of each hit; this part holds.

**Measured cost.** Maintainer facing: every build thread loads 26 lines more than the bar, and the scripts stand 70 over theirs. No verb's behaviour is affected.

**Closes when:** the seventeen scripts read at most 7,374 lines and the three documents at most 975, or Phillip retires the bars. By Phillip's decision of 2026-11-24 on #847, no further area card is filed for it. Ledger only.
