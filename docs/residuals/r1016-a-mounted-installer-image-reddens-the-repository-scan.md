---
title: A mounted installer disk image named for the assistant app makes the repository scan fail on every branch, and with it the battery and every mutation baseline
found: building R-1016, relay task 322, 2026-10-14.
issue: no
---

**The mechanism.** `scripts/scan_repo.py`'s runtime identity tier adds the
name of every entry under the macOS volumes mount root to the set of personal identifiers, on
the argument that a mounted volume is the contributor's. On 2026-10-14 a
read only installer disk image was mounted there under the assistant app's product name, the word this repository's agent instructions and skills use for it
 (the mount
root last changed 21:37), so that word became a personal identifier, and
every document, skill and test that names the assistant failed the scan:
`scan_repo.py` exits red and `tests/test_portability.py::
test_the_repository_itself_is_clean` fails, on `main` as on any branch,
with no line of the tree changed. Filtering the scan's output for that one
token left no other finding.

**Measured cost.** The battery is red for every unit while the image is
mounted, so the runner's gate refuses every merge. `scripts/mutate.py`
refuses to start on the red full baseline, and it scrubs `PYTEST_ADDOPTS`
on purpose, so the one environmental test cannot be deselected; R-1016's
table was recorded unmeasured for this reason. Ejecting the image, or a
`.scan-identity` that cannot remove a token, is the only remedy today, and
neither is a session's to take.

**Closes when:** the runtime tier ignores a mounted image that is not a
contributor's volume (a read only, quarantined disk image is the measured
shape), or declares a stop list of product and vendor names the repository
names by design, and the suite and scan stay green with the image mounted.
Ledger only: maintainer facing, and ejecting the image clears it at once.
