---
title: Intake's 42 owned test files are 402 lines over the card's target, the rest in the set verbs' suites
found: at the record of #864, U307, 2026-11-23.
issue: no
---

**The mechanism.** U307's brief asks the 42 test files it owns to come to at most 21,521 lines, from 29,083 on `c919209`. They stand at 21,923 on the branch head: 7,160 lines out, 402 short. The shortfall is in the set verbs' suites (`tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_set_progress.py` and the three account playlist suites, 5,367 lines before and 4,416 after against 3,971 for their share), where the builder that trimmed them judged the rest to carry assertions the recorded kills need. The last 34 lines came back when `test_a_fetch_that_raises_still_stops_the_watcher` was made deterministic so r924's F5 is killed every time.

**Measured cost.** None to a person and none to a guard: the test time target is met (the summed time of the 42 files down 43 and 38 percent in two alternated runs), every verb's behaviour compares equal, and every recorded kill is kept. The cost is #847's line target read on intake's tests, about two percent over.

**Closes when:** a later card that touches the set verbs' suites folds their remaining repeated setups (the account playlist and inspiration fixtures each file repeats) while the kill set replay stays at zero lost, or the final audit (#872) accepts the figure. Ledger only.
