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

---

## R-2022. The title analyze run gives a file with no title tag misses five shapes, each as main missed it

**Found:** at review round two of #995, U343, 2026-11-23.

**The mechanism.** Since review round one of U343, `analyze run` writes the
naming engine's headless title (the stem, a lossy marker set first) on a file
with no title tag, so `analyze adopt` can stamp the landed row
(`analysis/cli.py` `_untitled`). Round two drove five shapes it does not settle,
each behaving as origin/main does with its headed title:

1. A file the run does not measure, a name already carrying a head
   (`skipped-prefixed`) or one the detector cannot read (`skipped-undecodable`,
   a FLAC or M4A cut short), keeps no title tag; adopt leaves its row
   `title-tag-differs` on every pass, and the check counts it among the bare
   titles (the line says adopt names any it leaves).
2. A title the reader cannot read is overwritten by the stem: a FLAC whose
   first TITLE value is empty, an M4A whose title atom holds Latin 1 bytes.
3. An identifier stem (`92654769`) is titled with the identifier, so `name
   apply` composes `Artist - 92654769`, or holds a file with no artist as "not
   renamed to its title alone".
4. The library matcher misses a file with an artist tag and a title spelled
   `Artist - Title`, the title the stem gives (`acquire/match_library.py`).
5. `analyze run` pointed at a landed folder writes the stem as title onto a
   file the collection references, so its tag and its row disagree (main
   renamed such a file).

**Measured cost.** Driven on fixtures by the round two reviewer, every shape
identical on main but the fifth, where main's cost was larger. Whether a real
download or rekordbox produces the first four was not measured; nobody was
shown to point the run at a landed folder.

**Closes when:** each shape is given a title the landing lands (or is refused
by name), or recorded as accepted. Ledger only: no shape is new with U343.

---

## R-2023. analysis/separation.py's harmonic function has no shipped caller since the run stopped reading a key

**Found:** at the build of #995, U343, 2026-11-23.

**The mechanism.** `separation.harmonic` separated the harmonic part the key's
chroma was read from under the `whole` and `windows` key methods. U343 took
the key out of the run, so nothing under `src` calls it; only
`tests/test_analysis_separation.py` does. `separation.harmonic_percussive`,
which the energy measure calls, shares its module and stays used. Left in
place because the brief named the detector, the agreement and the check, not
the separation module, and its pins guard the energy's sibling.

**Measured cost.** None to a person: a function and its tests a maintainer
reads and keeps green for nothing. Its five tests that fail under librosa
1.0.1 on main and the branch alike are R-1633's, not this one.

**Closes when:** `separation.harmonic` and its tests are removed, or a later
unit names a caller for it. Ledger only, maintainer facing.

---

## R-2024. analyze run's answer still words a skip and a no answer by the head and the key it no longer writes

**Found:** at review round one of #995, U343, 2026-11-23.

**The mechanism.** Since U343 `analyze run` resumes on the `analyzed` mark and
measures no key, but its words are the old ones. A file skipped because it
carries the mark is reported `skipped-prefixed`, though its name carries no
prefix (`analysis/cli.py` `handle_run`, and `analysis/run.py` `run_batch`). A
detector that answers nothing settles a file `skipped-no-key`
(`analysis/light.py` `analyse`), a name from when None meant a keyless track;
the shipped detector answers None only without the analysis extra, which the
run refuses first. The answer's summary key is still `head_agreement` though it
carries the tempo's agreement alone. Kept on purpose: each is a word a reader
of the JSON answer, the reserved causes ratchet and the restamp's
`--scored-by` (which reads any status but `analyzed` as not scored) key on.

**Measured cost.** Driven by the reviewer: a second real run over seven marked
files answered `by_status: {"skipped-prefixed": 7, "skipped-undecodable": 1}`
over files with no prefix. A reader is told a prefix that is not there; no file
is written or skipped wrongly.

**Closes when:** the statuses are renamed (`skipped-measured` for a mark or a
head, a no answer word for `skipped-no-key`) and the summary key renamed, with
every reader of each moved in the same change, or a decision records keeping
them. Ledger only: a wording in a report, no file or row at risk.
