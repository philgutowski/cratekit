# Residual findings

Findings that are accepted but not yet fixed. The Definition of Done requires
this file to be current before each merge, so a known problem is a recorded
decision rather than something a future reader has to rediscover.

Each entry says what was found, why it was not fixed here, and what closes it.

The older findings are archived by number range in `docs/ledger/`, every entry
byte for byte as filed, and `board.py residuals --search WORDS` searches them
all. An amendment to an archived entry is made in its archive file.

---

## R-2021. A with vox playlist adopt apply recorded reads unexpected once the library has no vocal calibration

**Found:** at the review of #1022, R-1991, 2026-11-23.

**The mechanism.** `adopt apply` now records its vocal additions' playlists.
A recorded destination is compared on every check whatever this run derived,
and the check's own filter takes only the playlist signal dimension out of
`unexpected`, so with no calibration the recorded `with vox` playlist's tracks
read `unexpected`. A rebuild's record has the same shape for a vocal
destination it recorded while calibrated.

**Measured cost.** Driven at round one at the check: with a threshold the
tree converges, without one `unexpected:deep_house/with_vox:1`, where the
base said matching. Losing the calibration after an adoption filed a vocal
membership was not driven through a verb.

**Closes when:** the check leaves a recorded destination in a dimension this
run did not compare out of `unexpected`, as `left_behind` already does.
Ledger only, the reachability unmeasured.
