**The session before: the battery speed chore and the Phase G plan, `chore/battery-speed`, 2026-09-18.**
Attended, not a board unit. Four things landed together.
**The suite is parallel.** `addopts` carries `-n auto` and the dev extra carries
`pytest-xdist`. Measured on 11 cores at 7,678 tests: 532 seconds serial, 86 at
eight workers, 61 to 67 at auto, green each time including the disk image tests.
A venv older than this merge needs `pip install -e '.[dev]'` once. `-n 0` runs
in process, for a debugger. `scripts/mutate.py` inherits `addopts`, so its
baselines are parallel too. Its reporting plugin now writes from the xdist
controller only and reads the collected count off
`pytest_xdist_node_collection_finished`, and the driver scrubs the inherited
`PYTEST_XDIST_WORKER` identity from its child. Three tests in
`tests/test_mutation_driver.py` drive it against a fixture with `-n 2`. **The
driver has NOT yet run a real table under parallel workers**, so the first unit
to run one should read its null control and collected counts with that in mind.
**A product defect came out of the slowest test.** `listing.fetch_with_retry`
retried a `credential-missing` refusal five times and slept 31 seconds before
re-raising it, per listing. A `CratekitError` whose cause says
`retryable=False` now passes through on the first attempt, and a paired test
holds that a retryable refusal still climbs the ladder. No mutation table was
run over this change, it is two lines behind two new tests.
**The ledger gained R-413 to R-424**, twelve entries from the reads that planned
Phase G: the landing gap R-413, the rating scale hazard R-414, a correction to
R-400's wording R-415, the uncalled export routing writers R-416, six smaller
parity gaps, and the two entries issues 110 and 111 said they were owed, R-423
and R-424.
**METHOD changed.** Native Relay is in the loop and has a section. The
serialized order list is gone, spent. A board bar says which residuals earn an
issue, and a session now files that issue itself. The battery section says the
full suite is the merge gate and not the edit loop.
**The board gained Phase G**, units U67 onward, plus a card for every residual
that met the bar, from `docs/ideation/2026-09-18-parity-to-feature-complete.md`.
The two analysis tests near 30 seconds each spin a real process pool and were
left alone. Battery at the merge: ruff clean, 7,678 passed and 1 skipped, scan
clean.
