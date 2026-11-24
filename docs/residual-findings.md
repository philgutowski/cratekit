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

---

## R-2025. A machine named by a plain word is caught only in the host forms the scan lists, not a tailnet name, an unlisted suffix or a host typed in a shell prompt

**Found:** at the review of #1025, U957, 2026-11-23.

**The mechanism.** `_host_forms` in `scripts/scan_repo.py` lists the shapes
in which a detected ordinary word names the machine: `<t>.local`, `.lan`,
`.localdomain`, `.home.arpa`, `user@<t>`, `//<t>/` or `//<t>:port`, a UNC
`\\<t>\`, and `<t>:/path` or `<t>:~`. The base matched the bare word anywhere,
so every other form it used to catch now passes: a tailnet or router suffix
(`.ts.net`, `.fritz.box`), `.home` and `.internal`, which were tried and
removed because `Path.home()` and attribute access read as hosts, a default
shell prompt (`<user>@<t> ~ %` is caught by the `@` form, `<t>:~ <user>$` by
the scp form, but `[<t> ~]` is not), and a UNC path inside a source literal
with doubled backslashes.

**Measured cost.** Round one drove thirteen such forms: the base flagged all,
the first head none; the fix round restored the listed ones. The tree writes
none of the remaining forms today (grepped), so no producer was driven. The
other way, the `user@<t>` form reads `someone@somewhere` and `line@hours`
in two test files as hosts, so a machine named `somewhere` or `hours` is red
there (round two, through `scan_tree`); a URL host such as `https://host/x`
is red by design.

**Closes when:** a form that names the machine and not ordinary prose is
added to `_host_forms` with a test, after driving it over the tree for the
words the tree writes. Ledger only: maintainer facing.

---

## R-2026. A detected login or home name that is also a common word, such as a given name, passes the scan in prose

**Found:** at the review of #1025, U957, 2026-11-23.

**The mechanism.** `machine_identity_tokens` relaxes every detected token
whose lower case form is on `scripts/scan_ordinary_words.txt` to the path and
host shapes, the login and the home directory name as well as the hostname
and the volumes. SCOWL size 35 carries many given names in lower case as
common nouns or verbs (mark, frank, grace, rose, amber, heather among the
thirteen the review probed), so a contributor whose login is one of them is
caught at `/Users/<name>` and `<name>.local` but no longer in prose such as
"curated by <Name>".

**Measured cost.** Driven with the login and home patched to a probed given
name: the base flagged the bare name once, the branch not at all. No real
producer was driven; it is the price the brief sets on purpose, since the
same rule is what lets a machine named by a plain word pass.

A login or home name that is both on the list and a stand in segment
(account, example, library, music, name, somebody, someone, volume) is not
caught in its own home path either, since a stand in segment does not count
as naming the machine; round two drove `USER=music` over `/Users/music/...`:
round one's head reported it, the fix round's does not. The home directory
class already treats those segments as anonymous, so the cost is marginal,
the trade for `/Volumes/Music` in the docs.

**Closes when:** the login and home tiers are kept bare unless declared
otherwise, or the contributor declares the name in `.scan-identity`, which
the docs already advise. Ledger only: maintainer facing, nothing a DJ pays.

---

## R-2027. A Python attribute named local reads as a host form, so a machine named by a word the code uses as a variable stays red

**Found:** at U957, #1025, 2026-11-23, driving the words the brief's ten files share.

**The mechanism.** The `<t>.local` host form cannot tell `first.local !=
second.local` or `str(self.local / "config")` in code from a host name in
prose. A machine named by one of the words the tree writes as a variable
with a `local` attribute (first, second, other, self, area, among the words
driven) still fails the scan on those files.

**Measured cost.** Driven with the hostname patched to each word: the files
`tests/test_intake_land_rehearse.py` and `src/cratekit/core/rehearsal.py`,
and three mutation records quoting the latter, are red for those words. The
base was red for them too, bare, so nothing regressed; the brief's goal is
unmet for a machine named by one of them.

**Closes when:** the `.local` form refuses an attribute shape it can tell
apart (a following operator, method or path join) without missing a host in
prose, or the variables are renamed. Ledger only: maintainer facing.

---

## R-2028. a resort or rebuild resume refused because another driver holds the job carries the holder's findings so far as its own steps

**Found:** at the review of #1036, R-2020, 2026-11-24.

**The mechanism.** Each resume drives inside `ReportedDrive.owing()`, which
adds the after check's sentences, read from the committed item reports, to any
refusal raised there. `job-driver-held` is raised inside it, before this run
claims anything, so the refusal names what the other driver's finished trees
left and did not compare, counted so far while it keeps going. That is
against the rule `test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
states for the resort's calibration refusal (a run that drove nothing answers
for no tree). The resort did this on the base; the rebuild does it from
R-2020. `rebuilt` also turns `DriverHeld` into a plain `CratekitError`, keeping
its reason and exit code; no reader in the process tells them apart for these
verbs.

**Measured cost.** Driven with the driver lock held in process: exit 20,
`job-driver-held`, with the leftover and the not compared sentences of the one
committed tree as steps. True of that tree, and partial. Not driven with two
processes.

**Closes when:** `owing()` adds the steps only when this run claimed an item,
or the driver held refusal is raised before it. Ledger only.

---

## R-2029. a resort job an older build queued is told at its gate that the drive names the playlists not compared, and a drive over an older build's item reports names none

**Found:** at the review of #1036, R-2020, round two, 2026-11-24.

**The mechanism.** `routing_cli.UNRECORDED_UNREAD`, the gate's line over
facts frozen before R-2020, says "the drive names any it finds". A job the
older build already finished, or that this build finished, has no drive left,
and `--job` answers `ok succeeded` with no warning. And `rebuild.after_messages`
reads an item report with no `unidentified` key, which an older build's resort
worker wrote, as nothing unread, so a job left open with one tree done by the
older build names no unread playlist for that tree on either exit.

**Measured cost.** Driven: the base queued a job, this branch drove it (named
the playlist), and a second `--job` showed the gate's promise over a job no
drive was left for. A job the base itself finished was not produced (its
worker refused on volume identity in the harness). The second shape was
driven only with a stand in report; its producer needs two routed trees or a
crash window, and the shipped taxonomy derives one tree. The gate's line
already says the count may leave some out, so neither is a clean report.

**Closes when:** the line says a drive still to run names them, and a report
without the key is named as one that did not record them. Ledger only; it
closes by itself once no job queued before R-2020 is open.

---

## R-2030. the favorites step skipped warning reads every item the drive did not find done, and counting a done one too kills no test

**Found:** at the review of #1036, R-2020, 2026-11-24.

**The mechanism.** `rebuild.ReportedDrive.of` reads `driven`, the trees this
run drives, as every item not yet done, and only the favorites step skipped
warning (U132) reads it. The round one review changed the filter to keep every
item, done or not, and no test died; the base's two resumes read the same
filter and had the same gap.

**Measured cost.** None measured: a job continued with a tree already done and
a taxonomy whose favorites class is missing would name that done tree's skipped
step again, which is true of the tree and only says it twice. Not driven.

**Closes when:** a resume over a job with one tree done and one pending, under a
taxonomy with no favorites class, asserts the warning names only the pending
tree. Ledger only.

---

## R-2031. the rebuild and resort workers build and stage their item report after the write landed, so a failure there fails an item whose write is done

**Found:** at the review of #1036, R-2020, 2026-11-24.

**The mechanism.** `cli/rebuild.handle` and `routing_cli.handle_resort` call
`rebuild.after_report`, which loads the taxonomy again, and stage the report
under the queue store, after `rebuild_governed_tree` committed the membership
and cleared the flag. A raise there (an unreadable taxonomy, a queue store
that cannot be written) fails the item over a write that landed, and a resume
drives the tree again, which adds nothing the second time. The resort had this
shape on the base; the rebuild has it from R-2020.

**Measured cost.** Not driven: the producer, a queue store that refuses a write
between the commit and the staging, was not built.

**Closes when:** the report's inputs are read before the write, or a failure
staging it is said rather than failing the item. Ledger only.

---

## R-2032. the playlists a resort or rebuild did not compare are named without their tree, so two trees' same named playlists read as one name twice

**Found:** at the review of #1036, R-2020, 2026-11-24.

**The mechanism.** `rebuild.unidentified_message` names each playlist as
`FOLDER/PLAYLIST`, the way `crate converge` names it inside one tree's line.
The resort's gate facts and `rebuild.after_messages` gather every tree's
playlists into one list, so over two routed trees holding a playlist of the
same folder and name the sentence says that name twice, "under the tree", and
a person cannot tell which tree each is under.

**Measured cost.** Driven only with a stand in: a second process continuing a
rebuild over the same tree twice named `Loud! Room/Unsorted` twice. A library
whose taxonomy derives two routing trees, each with such a playlist, was not
driven; the shipped taxonomy derives one.

**Closes when:** each entry carries its tree where more than one tree is named,
or the day a taxonomy derives two trees. Ledger only.
