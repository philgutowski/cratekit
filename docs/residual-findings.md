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

---

## R-2033. A mutation row on a part of the verb table derives the full suite as its subset

**Found:** at the review of #977, U328, round one, 2026-11-23.

**The mechanism.** A row with no `tests` of its own is given the test files
that import the mutated module (`mutate_table.derive_subset`). 91 test files
import `cratekit.cli.registry`; no test imports a part, since a verb is read
through the registry, so a row on `cli/registry_*.py` falls back to the full
suite.

**Measured cost.** Driven by the reviewer through `derive_subset`:
`cli/registry.py` gives 91 test files and each of the five parts the full
suite. The fallback is the safe direction, so no kill is missed; the cost is
a full run, about seven minutes on the cloud container, for each row a later
card writes on a verb's entry without naming its tests. Not timed on a real
row. The 35 replayed rows carry the tests their recorded kills name.

**Closes when:** `derive_subset` reads a part of a split module as its
module, the registry's parts by `cli/registry.py`'s own imports, or the rule
for a row on a part is written where rows are written. Ledger only.

---

## R-2034. No battery check holds the 1,500 line bar on a source file, and two files sit within eight lines of passing it

**Found:** at the build of #977, U328, 2026-11-23.

**The mechanism.** Point 2 of #847, U290, asks that no source file under
`src/cratekit` outside `_vendor` pass 1,500 lines. The measure,
`scripts/refactor_measure.py lines --files`, prints the files over it, and
nothing in the battery runs that reading: `cli/registry.py` stood at 2,459
lines and then 2,544 under a green suite until an audit measured it. U328
split the registry and added a test that holds the registry and its parts to
the bar (`tests/test_cli_contract.py`), and holds no other file, since a check
over every source file would redden cards building beside it.

**Measured cost.** None to a person using a verb. On the head U328 merged,
`core/review.py` is 1,495 lines and `cli/setup.py` 1,493, so six more lines
on the first or eight on the second pass the bar with the suite green, and
the next audit of #847 finds point 2 short again. The next four are `intake/native.py` 1,438,
`modules/tools/backup.py` 1,429, `core/cause.py` 1,419 and
`label/sync_cli.py` 1,409.

**Closes when:** a battery test fails on any file under `src/cratekit`
outside `_vendor` over `LARGE_FILE`, landed when no card that grows one of
the two files is building, or the audit card of #847 decides the bar is read
at audits only. Ledger only: a maintainer facing count.

---

## R-2035. The two text readers of the verb table pool tuple and constant names across its files, and the board's reads every registry file on disk

**Found:** at the review of #977, U328, round one, 2026-11-23.

**The mechanism.** `scripts/refactor_measure.py` `verbs_from` and
`scripts/board.py` `planned_units` read the verb table as text, the registry
and its `registry_*.py` parts together since U328. Both keep one mapping of
names for all the files, the last file read winning, where Python binds a
name per module. And `planned_units` reads every `registry*.py` under
`src/cratekit/cli` whether `cli/registry.py` assembles it or not.

**Measured cost.** None on the tree: no part binds a string constant, each
part holds one tuple under its own name, and a test holds each reading to the
live registry. Driven by the reviewer on fixtures: a constant bound in two
parts gave `{2: ['m.a', 'm.b']}` where Python gives units 1 and 2; a second
`ENTRIES` tuple in a `registry_tools.py` replaced the table with no refusal;
a tuple that stars itself ends in `RecursionError` where the base raised
`ValueError` (Python cannot import that source either); a `registry_old.py`
nobody imports, holding a marker, was read as owing a unit; and a half
written `registry_wip.py` ended `planned_units` in an uncaught `SyntaxError`,
as a half written `registry.py` did at the base. The producer of each is a
file nobody has written.

One file over, and the same at the base: `planned_units` has no refusal for
a tree with no `cli/registry.py` and returns no unit owed, so `board.py
closing` would pass a trailer over a register it could not read. The live
table holds no `planned_in` marker today, so the test that holds that reader
to the live registry compares empty with empty; U328's fixture test is what
reads a marker.

**Closes when:** both readers resolve a name in the file that uses it and
refuse a name two files bind, and `planned_units` reads the parts
`registry.py` stars and no other file and refuses a tree with no registry.
`refactor_measure.py` has three lines left under its 1,500 and the seventeen
scripts of #979's bar thirteen under 7,374 (`board.py` 26 under its own
1,500), so it waits on room there. Ledger only.

---

## R-2036. The seventeen scripts of U330 passed 7,374 lines on main, by the privacy scan's host forms

**Found:** at the last merge of main into #977, U328, 2026-11-24.

**The mechanism.** Point 6 of #847, U290, holds `scripts/` to the standard
U330 (#979) set: the seventeen scripts its brief names total at most 7,374
lines. U330 left them at 7,360. U957 (#1025) landed `scripts/scan_repo.py`'s
host and path forms for an ordinary word, 164 lines, and nothing in the
battery holds the total, so it passed the bar under a green suite.

**Measured cost.** `wc -l` over the seventeen files the brief of #979 lists:
7,327 at `e0573a66` and 7,443 at `c5fb1015`, both on 2026-11-24, 69 over.
U328 adds 1, in `scripts/board.py`, so its merged head reads 7,444. No file
in `scripts/` is over 1,500 lines. None to a person using a verb.

**Closes when:** the audit card of #847, #987 (U338), measures point 6 again
and files a further card for the total, or Phillip moves the bar for the
scan's new forms. Ledger only: a maintainer facing count.

---

## R-2037. The source total passed 193,000 lines on main while the further cards of U290 built, by feature cards

**Found:** at the build of #977, U328, 2026-11-23.

**The mechanism.** Point 2 of #847, U290, asks that `src/cratekit` outside
`_vendor` end at or under 193,000 lines. The final audit (#872, U315) read
188,904 on `d289f61` and held that half of the point. Feature cards kept
landing while the further cards built, and nothing in the battery holds the
total, so it grew past the bar under a green suite.

**Measured cost.** `scripts/refactor_measure.py lines`, and `wc` over the
tracked files for the earlier commits: 188,904 at `d289f61`, 190,196 at
`392a2d1`, 191,607 at `4d1ff8b9`, 191,899 at `c84dc4ac`, 192,016 at
`99e0cbc0` and 193,136 at `2e8681d1`, all on 2026-11-23, then 193,253 at
`e0573a66` and 193,382 at `c5fb1015`, the base U328 merged on. U328's
split of the verb table adds 107 more, the five parts' heads and the
assembly, so the head it merged reads 193,489, 489 over. None to a person using a verb.

**Closes when:** the audit card of #847, #987 (U338), measures point 2 again
and files a further card for the total, or Phillip moves the bar for the
features added since. Ledger only: a maintainer facing count.

---

## R-2038. A name a listed module re-exports is bound twice, so a test that patches its origin does not reach a caller reading the listed module

**Found:** at review round one of #980, U331, 2026-11-23.

**The mechanism.** U331 routes each feature package's reach into an unlisted core module through a listed module that re-exports the names, `from cratekit.core.snapshot import assert_room_for_check as assert_room_for_check` in `core/session.py` among them (`session` for `preflight`, `processes` and `snapshot`, `config` for `profiles`, `jobs` for `discovery`, `pool` for the cores' ceiling, `active_taxonomy` for `foreign_tree`). Each is a second binding of the same object. A caller in a feature package now reads `session.assert_room_for_check`, so a test that monkeypatches `snapshot.assert_room_for_check` changes nothing that caller sees.

**Measured cost.** Maintainer facing. Round one found the room test patched the name it was meant to hold, and it now takes the room away below both bindings. `tests/test_import_rules.py` asserts every re-exported name is its origin's object, which holds the bindings equal at import and not under a patch. No user facing cost was driven.

**Closes when:** a test of a re-exported guard patches what both bindings call, or the rules name each re-export a patch must reach. Ledger only.

---

## R-2039. The doctor's help sits two modules under its ceiling, and a top level import of active_taxonomy on its path costs both

**Found:** at the merge of main into #980, U331, 2026-11-24.

**The mechanism.** `tests/test_cli_lazy.py` holds `crate doctor --help` under a ceiling of cratekit modules, 90 when this card measured it and 95 since U328 put the registry's table in five parts that load at every start. Round one put the foreign tree's names on `core.active_taxonomy`, so every module importing `active_taxonomy` at its top loads `core.foreign_tree` too. With U343 merged the help reached 90 and the test failed. `cli/doctor_state.py` and `core/taxonomy_upgrade.py` now import the loader in the one function that reads it, and the help loaded 88; with U328 merged it loads 93 of 95.

**Measured cost.** Maintainer facing. Two more modules on the doctor's import path, or a top level import of `active_taxonomy` put back in either file, which costs two, fail the test again. The mutation table holds both imports (rows S13 and S14).

**Closes when:** the doctor's help is measured with a margin a unit can spend, or its imports are cut further. Ledger only.

---

## R-2040. modules.outbound is no toggle's home, so the rules for a toggleable package no longer read it

**Found:** at the build of #980, U331, decided by 980-toggle-homes-1 on 2026-11-24.

**The mechanism.** `TOGGLE_HOMES` in `tests/test_import_rules.py` named `cratekit.modules.outbound` as one of `export`'s homes, and the whole `cratekit.favorites` package as `favorites`'. The registry gates one verb with `favorites`, `sync favorites` in `favorites/cli.py`, and the four export verbs with `export`. The rest of the favorites package builds four verbs no toggle gates and part of the landing, and `modules.outbound` is called by organize, sync, label, intake and the favourites sweep. With either toggle off, five ungated verbs could not build: five of the seven dangling lines main allowed. Phillip's decision, option 1, narrowed the table to what the registry gates: `favorites` owns `cratekit.favorites.cli` and `export` owns `cratekit.export`. No source file moved.

**Measured cost.** Maintainer facing. An always on package could import `modules.outbound` at its top level and no test of the import rules would fail, since it is no toggle's package any more. No verb's output changes.

**Closes when:** `modules.outbound` is split into what `export` owns and what every caller uses, and the ungated parts of `cratekit.favorites` move out of it, so each package belongs to one toggle (the decision's option 2, a restructuring card of its own with its own replay). Ledger only.

---

## R-2041. Three refusal origins name the package their module left

**Found:** at review round one of #980, U331, 2026-11-23.

**The mechanism.** U331 moved `analysis/check_cli.py` and `analysis/rekordbox_check.py` to `intake/`, and `core/rehearsal.py` to `intake/`. Their `_ORIGIN` tuples were kept as they were, `("analysis.check_cli",)`, `("analysis.rekordbox_check",)` and `("core", "rehearsal")`, since the card freezes what every verb prints, and the envelope prints the origin. Tests pin each one.

**Measured cost.** A refusal from `analyze check` or `intake land`'s rehearsal names a module path that no longer exists. A maintainer reading `cause.origin` looks in the wrong package. No user facing cost: the origin is a diagnostic field, and its text is what it always was.

**Closes when:** a card allowed to change printed output renames the three origins with their pinning tests. Ledger only.

---

## R-2042. analyze check and analyze vocals build without the analysis package and cannot run without it

**Found:** at review round one of #980, U331, 2026-11-23.

**The mechanism.** U331 made both verbs build with the `analysis` toggle's homes blocked by importing their analysis helpers at call time: `intake/rekordbox_check.py` takes `cratekit.analysis.agreement` inside the two functions that read it, and `vocals/cli.py` takes `cratekit.analysis.cli` and the loader's module inside the functions that call them. So rule four and the drive of each toggle off read both verbs as built. A run that reaches those functions still imports the package.

**Measured cost.** Not driven against a real install: no profile removes the analysis package's source, which every install ships, so no producer of a missing package was found. A toggle off hides the package from the import rules' drive, not from the interpreter.

**Closes when:** the helpers both verbs borrow move to a package no toggle owns, or the rules read a call time import of a toggle's home as a dependency of the verb. Ledger only.

---

## R-2043. A module handed over other than by a top level import is not followed by the import measure

**Found:** at review round one of #980, U331, 2026-11-23.

**The mechanism.** `scripts/refactor_measure.py` follows a name that is a module into that module, so `tags.art.read` and `from cratekit.core.tags import art` read as uses of `cratekit.core.art`. It follows only what a top level import hands over, through as many modules as pass it on by import. A module bound by an assignment, a star import, `getattr`, a function that returns it, a conditional import or an import inside a `try` is not followed, so a feature package could reach an unlisted module through a listed one under a single counted name.

**Measured cost.** Maintainer facing. Round two scanned the 25 listed modules at runtime and found none holding a module bound any way other than a top level import, so nothing in the tree uses an unfollowed spelling today.

**Closes when:** the measure reads the listed modules' runtime bindings beside their source, or the rules refuse a module attribute on a listed module that is not a top level import. Ledger only.

---

## R-2044. The toggle drive test drives four hand listed toggles of sixteen

**Found:** at review round two of #980, U331, 2026-11-24.

**The mechanism.** `tests/test_import_rules.py::test_with_a_toggle_off_every_remaining_verb_builds_and_formats_its_help` blocks the homes of four toggles it lists by hand, builds every remaining verb and formats its help, in a fresh interpreter. The other twelve toggles are read by the static rule alone, which follows top level imports. An import only a run makes, `importlib.import_module("cratekit.label.cli")` at the top of `sync/cli.py`, leaves the test green with `labels` off; the same line naming `cratekit.vocals.cli` fails it.

**Measured cost.** Maintainer facing. A verb left dangling by a dynamic import under one of the twelve toggles passes the suite. Round two found no producer in the tree: the static reading and a drive of every toggle both read 0. Driving all sixteen takes 25.8 s against about 8 s for the four, over METHOD's ten second bar for a test.

**Closes when:** every toggle is driven in a time under that bar, or `refactor_measure.py imports --drive` runs in the battery. Ledger only.

---

## R-2045. Three guards of the import measure kill nothing, a plain import inside a function, a chain past a second handed module, and the drive formatting help

**Found:** at the mutation table of #980, U331, 2026-11-24.

**The mechanism.** Three rows of `docs/mutation/u331.md`, each on `scripts/refactor_measure.py` and each promoted to the full suite, read zero. M02 lets a plain `import cratekit.x` inside a function hand its module over, as if it were a top level import; the tests hold the same rule for a `from` import inside a function (M03, killed) and not for this spelling. M08 stops `Tree._reached` at the first module handed on, so a chain read past it is not followed further; no fixture reaches a module through two handed modules in one chain. M09 drops `parser.format_help()` from the script's `imports --drive`, which no test runs: the battery's own drive test in `tests/test_import_rules.py` formats help itself.

**Measured cost.** Maintainer facing. A regression in any of the three would let the measure read a reach off the list, or a dangling verb, as clean, while the battery's own rules, which share the reading, stay green over the same fixtures. Not driven against the tree: the measure reads 0 reaches off the list and 0 dangling verbs on the branch either way.

**Closes when:** a fixture test in `tests/test_refactor_measure.py` holds each reading, a lazy plain import, a chain through two handed modules, and a drive whose builder succeeds and whose help fails. Ledger only.

---

## R-2046. A replay row names a test a later unit renamed away, and its batch then measures nothing

**Found:** at the kill set replay of #984, U335, 2026-11-24.

**The mechanism.** `killset.py`'s `tests_of` keeps a subset entry whose file exists, without asking whether its test does. Rows u135 A8 and A12 name `test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set` and `test_inspiration_join_stays_pinned_beside_the_inbox_join` in `tests/test_u135_set_inbox_join.py`, which no longer define them, so the subset collects nothing and `mutate.py` refuses the whole batch with NOTHING MEASURED. The load calls (`load_spec`, `load_mapped`, `refuse_unrecorded_sources`) and a collect of the union of a batch's subsets both pass over it.

**Measured cost.** One helper container's run of before batch five, about twenty minutes, before the two rows were pointed at their file and the batch restarted.

**Closes when:** `killset.py rows` drops or widens to its file a subset entry whose node id does not collect, or the driver's load check collects each row's subset. Ledger only: maintainer facing.

---

## R-2047. One case of the sync pair merge fold runs the same merge as another

**Found:** at the review of #984, U335, 2026-11-24.

**The mechanism.** `test_the_side_that_leads_the_order` in `tests/test_sync_pair_merge.py` holds the cases `with_no_change..._leads_again-rekordbox` and `the_stopped_writes_order_is_not_read_against_the_base-stopped` with identical parameters. The base ran the same merge in the two tests they were folded from, so the fold kept every assertion and one case is redundant.

**Measured cost.** One merge run twice, under a millisecond; no guard lost.

**Closes when:** one of the two cases is given the input its base test's name describes, or the two are named as one. Ledger only.

---

## R-2048. Test slice four is 7.95 percent smaller, short of its 59,053 line bar and of the 13.97 percent share

**Found:** at the build of #984, U335, 2026-11-24.

**The mechanism.** The brief fixed the slice at 95 files and 68,640 lines on `d289f61` and its bar at 59,053. By the card's start eleven new test files had landed inside the same path range (U339, U340, R-1716, R-1950, R-1991, R-2020) and the old files had grown, so the range held 106 files and 74,245 lines. Eight builders trimmed it to U312's rules, folds through parametrize, shared helpers and builders, prose cut to the rule and its reason, with no blank line removed inside a test body and no statement packed, and reached 68,342: 5,903 fewer, 7.95 percent (per run of files 3.2, 4.9, 11.0, 9.0, 9.0, 9.3, 7.0 and 10.2 percent). Each stopped for the reason R-1941 gave: docstrings were already one line (3,276 docstring and 1,611 comment lines of 74,245), and the tests are distinct scenarios whose setup differs, so a fold needs a branch per row, and every helper pays its own def, docstring and two blank lines.

**Measured cost.** The slice is 9,289 lines over the brief's bar and 4,469 over the share floor of 63,873. No person using a verb pays for it; the epic's point 5 line bar stays missed by this slice's share.

**Closes when:** the audit card of U290 (#987, U338) settles point 5's line bar against the suite as it now stands, by a measure that does not count the separating blank lines PEP 8 requires, or by a card that removes whole tests a stronger test covers. Ledger only: maintainer facing.

---

## R-2049. The title differential's corpus is the tagging tests' string constants, so a test trim moves it

**Found:** at the review of #984, U335, 2026-11-24.

**The mechanism.** `scripts/title_differential.py` builds its corpus from every short string constant of fifteen tagging test files. A trim that folds tests or renames a fixture's file names changes that corpus: on this branch `corpus()` read 2,248 strings on the base and 2,318 on the head, 8 lost (among them the file names "a dance record" and "a disco record" of the remap fold) and 78 gained, mostly parametrize ids.

**Measured cost.** None measured: the script is a differential research tool run by hand, exits 0 always, and is not a verb. A later run compares a slightly different corpus than an earlier one.

**Closes when:** the corpus is a fixed data file the script owns, or the record of any run names the commit its corpus was read at. Ledger only: maintainer facing.

---

## R-2050. A replay row widened to the full suite can record an unrelated death as its kill

**Found:** at the kill set replay of #981, U332, 2026-11-24.

**The mechanism.** `scripts/mutate.py` promotes a row whose subset kills
nothing to the full suite, and counts any death there as the row's kill.
`u317.Q10_token_not_struck` (`_strike_token(cfg)` to `pass` in
`src/cratekit/modules/tools/backup.py`) names `tests/test_backup_quick.py` as
its subset, which errors at setup on a container without rclone, so the
driver widened it. In U332's before batch 1, on `324cafa`, the full suite
recorded one death,
`tests/test_jobs.py::test_everything_the_queue_writes_is_owner_only_under_any_umask`,
a test that drives only the job queue and never reaches the backup. The after
batch, whose row named that file, widened too and recorded none, so
`killset.py check` reads the row as lost. Two later full suite runs of the same
mutation on the base killed nothing, so the death did not reproduce: one
intermittent failure became a recorded kill.

**Measured cost.** None to a person using the verbs. The row's own killers,
`test_a_failed_run_by_another_installation_makes_the_next_run_full` and
`test_a_run_that_fails_strikes_the_token_from_the_library_fact`, kill it on
both sides once rclone is present (`docs/mutation/u332-replay-q10-rclone-before.json`
and `-after.json`, `check` exits 0 on the pair). The cost is a maintainer
reading a lost kill that is not one, and the reverse: a kill recorded on an
intermittent death stands for a guard no test holds.

**Closes when:** a promoted row's death is confirmed by running the dying
tests again under the mutation, or a death in a test that never imports the
mutated module is reported apart from the kill. Ledger only: maintainer facing.

---

## R-2051. Test slice 1 ends 3.5 percent smaller, not 14, because structure alone gives no more

**Found:** at the build of #981, U332, 2026-11-24.

**The mechanism.** #981 asked slice 1 of the test tree (the 200 files from
`tests/__init__.py` to `tests/test_catalogue_app.py` in path order, 73,259
lines at `55e958b`) to end at or under 62,155 lines, so the four slices
together bring `tests/` under point 5's bar of 249,132. Eight builders cut it
by Phillip's answer A on #847: parametrize folds, shared setup within a file
or a support file of the slice, deleting a test only where another checks all
it checks, and prose cut to the rule and its reason. They reached 70,702 by `scripts/refactor_measure.py lines`, 2,557
lines fewer. Every builder stopped short and measured why (1.6 to 7.0 percent
per group): the tests left are distinct end to end scenarios whose setup
differs test to test; a table of strings is as long as the tests it would
replace; the prose left is almost all one line reasons, residual titles and
decisions; and 5,189 lines are not the card's to cut (`tests/conftest.py`,
`tests/_pending.py`, the reserved cause pins). About 13,600 of the slice's lines
are blank, mostly the two between top level definitions. The cuts that would
reach the number are formatting (dropping those blank lines, joining calls
already split over lines) or deleting tests that still guard something, and the
card took neither. R-1941 measured the same wall across the whole suite.

**Measured cost.** None to a person using the verbs. Point 5 of #847 stays
unmet by about 8,547 lines in this slice; the question on #981 asked Phillip
how to treat the miss, and the card took the recommended option, land with
the miss named.

**Closes when:** the audit card after the four slices (#987) settles point 5,
by a decision to accept what structure gives, to lower the bar, or to count
lines another way. Ledger only: maintainer facing.

---

## R-2052. Slice three of the test trimming is cut by a third of its share, since what is left is layout

**Found:** at the build of #983, U334, 2026-11-24.

**The mechanism.** #983 owed the 104 test files from `tests/test_label_playlists_kept.py` to `tests/test_restore_cli.py` a cut to at most 62,948 lines (16.4 percent of the 75,260 the range held at `55e958b`, four files having joined it since the brief's `d289f61`). Eight builders cut it from structure and prose to 71,656, 4.8 percent, with every test still running and every assertion kept: the groups reached 0.9, 5.95, 1.54, 1.28, 7.7 (7.6 after a three line fix to one of its files), 2.95, 6.0 and 14.09 percent. Each measured why it stopped: docstrings were already one line, exact repetition inside a file is a few percent of logical lines, and a parametrize case costs two to four lines against the five to eight of the test it replaces, so folds of short tests break even. Of the 71,656 lines left, 14,219 are blank, 5,759 of them the second of PEP 8's two between top level definitions, and several hundred are test signatures wrapped because the test's name is a sentence.

**Measured cost.** Point 5 of #847's definition of done stays unmet by 8,708 lines in this slice. No person using the verbs pays anything; the suite is as strong as before.

**Closes when:** the epic's audit decides what point 5's line bar should be measured against, or a card the audit files reaches it some other way. The question on #983 offered a blank line cut and a test rename card as options and took the recommended one, landing the gap named. Ledger only: maintainer facing.

---

## R-2053. The mutation driver writes killing node ids as pytest names them, so a table quoting the portability guard's planted values fails the scan

**Found:** at the kill set replay of #983, U334, 2026-11-24.

**The mechanism.** `tests/test_portability.py::test_guard_covers_every_shipped_surface` is parametrized over planted offences, a home directory and access tokens among them, and pytest writes each case's values into its node id. `scripts/mutate.py` records the killing node ids whole in the table's `.json` and `.md`, so a replay row that test kills, `u28-skills-independent.X1_placeholder_exemption`, carried the planted home path and token into `docs/mutation/`, and `scripts/scan_repo.py` and `test_portability.py::test_the_repository_itself_is_clean` refused the tree. U334 wrote those values as placeholders by hand, as the u313 tables had done.

**Measured cost.** One red battery on the branch, caught before the merge; a maintainer hand edits a measured table. Nobody using the verbs pays.

**Closes when:** the driver writes a killing node id through the scan's own placeholder rule before recording it, or the guard's case ids are given by `ids=` naming the offence rather than its text, with a test that a replay of that row passes the scan. Ledger only: maintainer facing.

---

## R-2054. The mutation driver runs under an inherited SIGINT ignore and says nothing, so an interrupt guard's kill reads zero

**Found:** at the kill set replay of #983, U334, 2026-11-24.

**The mechanism.** `scripts/mutate.py` and `scripts/cloud_battery.py` measure in whatever signal dispositions their process inherited. Started under `nohup` and a shell's `&`, SIGINT is ignored, every pytest child and every pool worker inherits that, and a mutant that removes `src/cratekit/core/pool.py`'s own `signal.signal(signal.SIGINT, signal.SIG_IGN)` in the stream worker survives `tests/test_pool_stream.py::test_the_terminals_interrupt_does_not_kill_a_stream_worker`. Neither the table nor its markdown records the disposition, so the zero reads as a lost kill.

**Measured cost.** One row of 2,592 in U334's replay, `u241.M01_worker_takes_the_interrupt`, read zero in after batch 4 and was measured again as a one row batch, killed on both sides. Maintainer facing: a false loss costs a re-measure, and a false zero on a new row would read as a guard nothing kills.

**Closes when:** the driver records the SIGINT disposition it measured under and refuses, or resets SIGINT to the default before its first run, when the inherited one is ignored, with a test that starts it so. Ledger only: maintainer facing.

---

## R-2055. The restore suites' tests that fail on Linux were moved onto shared fixtures and checked only by reading

**Found:** at the review of #983, U334, 2026-11-24.

**The mechanism.** 26 tests in `tests/test_restore_cli.py` (no `rclone` on the container) and 8 in `tests/test_restore.py` (root ignores a directory's mode, and one backup restore) fail on every Linux container and are on the base's known failures. #983 moved them onto the fixtures and helpers it added in those files (`acked`, `record`, `remote_log`, `scratch`, `target`, `seams`, `decided`, `_refusal`, `_one_session`, `_recover`, `_two_acts`, `_refused_as`). The review compared each against `main` and found the same calls in the same order with the same arguments, but none of them could be run to a pass here, and a kill whose only killer is one of them cannot be seen by the Linux replay either.

**Measured cost.** Not driven: on Linux they fail before and after for the machine's reasons, the same 34 ids. If a rewrite were wrong, a macOS battery would show it as newly failing there.

**Closes when:** the macOS battery runs these two files on the merged tree and reports the 34 tests passing as they did on `main` at `55e958b`. Ledger only: the check is owed at a local sitting, already in the record's OWED paragraph.

---

## R-2056. converge and the rebuild derive the vocal sub from the file's score though U127 gave it to the vox My Tag, so a track adopt apply files by its tag reads as a leftover

**Found:** at sitting 107, 2026-11-24, A226's live converge read on a copy of the live database.

**The mechanism.** R-841 closed on 2026-10-10 with the author's decision that the `vox` My Tag owns the vocal sub (U127). `adopt apply` files the vocal sub from that tag (`adopt.placements.vox_tagged`, `adopt.plan.vocal_sub`). The derivation the convergence check, `tree rebuild` and `route resort` share still files it from the file's `voxlevel` against the calibrated cut (`rebuild.derive_from_taxonomy`, `routing.routes_with_vox`). So a track tagged `vox` whose file reads under the cut is placed by adoption and named `unexpected` by the check, and `route resort`'s left behind list names it for a person to take out by hand. In reverse, a file over the cut with no tag is placed by the derivation and never by adoption.

**Measured cost.** On a copy of the live database (sha256 head 2b7393041132680c) with every file's `voxlevel` read, cut 3.0: 1,759 rows tagged `vox`; **2 tagged rows read under the cut**, one of them Sworn Virgins, Fifty Dollar Bills, which A229's live `adopt apply` put into Nu Disco / Indie Dance / with vox on 2026-11-23 and which `crate converge` on 2026-11-24 lists as `unexpected:nu_disco_indie_dance/with_vox`; **607 rows read over the cut with no tag**, every one already in a with vox playlist, which converge reads as correct and the tag's rule does not place. So the product's own check calls a membership its own adoption wrote, by the rule the author chose, a leftover. Driven end to end on live data.

**Closes when:** one signal places the vocal sub on every path: the derivation reads the tag as U127 decided, or the check accepts a with vox membership the tag places, and the 607 untagged rows are either tagged or named. Earns an issue under the board bar's (b): a report says something false about a membership the product itself wrote.

---

## R-2057. A playlist whose live rows read 1 to N while a row marked removed holds one of those places is never planned by the repair

**Found:** at the review of #1058, U958, round two, 2026-11-24.

**The mechanism.** `crate repair numbers` plans only a playlist whose live rows
are not 1 to N, as the card asks ("a contiguous playlist is never written").
A row marked removed that shares a live place (rekordbox's own renumbering
after a hand removal leaves one, sitting 107: a marked row at 55 under live
rows renumbered 1 to 555) is moved to 0 only when a product add or removal
next touches the playlist; until then the doctor row reads OK. `read_back` and
`gap_violations` would call the same state a failure, since they judge a
playlist the repair or a removal wrote.

**Measured cost.** Driven on the repair suite's fixture: a playlist 1, 2, 3 with
a marked row at 3 plans nothing and the doctor reads OK. Whether rekordbox's
Remove from Playlist can take a marked row that shares the shown position's
number is unmeasured.

**Closes when:** the attended card's hand removal reads such a playlist, or the
repair plans a playlist with a marked row on a place. Ledger only.

---

## R-2058. The closing up counts a live membership of a track marked removed from the collection as a place, and whether rekordbox shows that row is unmeasured

**Found:** at the review of #1058, U958, round one, 2026-11-24.

**The mechanism.** `rb_positions.contiguous_positions` and `numbering` read a
membership row as live from its own `rb_local_deleted` alone. A live membership
whose content row is marked removed (a cloud sync tombstone, R-675's shape) is
numbered as a place. `playlist_pair.members` leaves such a row out of what it
says rekordbox shows. If rekordbox does not show it, the shown positions skip
it, and the closing up leaves the numbers one off from the positions after it,
the defect U958 closes.

**Measured cost.** Driven by the round one review on a disposable library with
member 2's content row marked removed: the numbering read the playlist 1 to 4
as contiguous and the doctor row read OK, while `playlist_pair.members` showed
three rows. What rekordbox shows for such a row was not measured; no product
code marks a content row removed while keeping its memberships.

**Closes when:** an attended sitting reads whether rekordbox shows a live
membership of a track marked removed from the collection, and the rule counts
or skips it to match. Ledger only.

---

## R-2059. A membership row this product marks removed is put at TrackNo 0, and what rekordbox does with a marked row at 0 is unmeasured

**Found:** at the build of #1058, U958, 2026-11-24.

**The mechanism.** `rb_positions.close_gaps`, run by `commit_guarded`, numbers
the live rows of every playlist a membership removal touched 1 to N and moves
every row marked `rb_local_deleted` 1 in that playlist to `TrackNo` 0, its
`TrackNo` alone, so no marked row shares a place with a live one. `crate
repair numbers` does the same over the playlists it plans. Sitting 107 (A218)
showed rekordbox leaving a marked row at 55 out of the shown positions, so a
marked row is not counted as a place; nothing measured rekordbox reading,
syncing or removing around a marked row at 0. A row at 0 was chosen because
rekordbox's Remove from Playlist takes the row numbered as the shown position,
which is never 0, and a marked row left on its old number would share a place
with the live row closed up onto it.

**Measured cost.** Not driven against rekordbox, which no cloud session may
open. On fixtures every reader in src skips a marked row, and `add_memberships`
appends past the highest number over every row, so 0 changes no append.

**Closes when:** the attended card's hand removal reads a playlist the repair
closed up, holding a marked row at 0, before and after, and rekordbox removes
the selected track and leaves the marked row as it was. Ledger only: it closes
only at an attended sitting.

---

## R-2060. With two live playlists of the favourites source's name, the repair and the doctor row leave the Favorites folder out and still read clean

**Found:** at the review of #1058, U958, round two, 2026-11-24.

**The mechanism.** `write/numbers.scope` takes the folder holding the
favourites class's source playlist into scope only when exactly one live
ordinary playlist outside another app's folder carries the name, as the
favourites verbs require (U119), so a namesake in a person's own folder never
pulls that folder in. With two, neither folder is read, and the doctor's
`library.playlist_numbers` line counts only what is left: round two drove a
gapped `Favorites / 2026-10` reading INFO with one `All Favorites` and OK,
"all 0 playlists", after a second was made under another folder.

**Measured cost.** Driven on the repair suite's fixture. The producer, a
person making a second playlist of the source's name in rekordbox, was not
driven; the favourites verbs refuse loudly in that state, so the person is
told there, not here.

**Closes when:** the scope holds both candidate folders back and the plan and
the doctor line name them, as a playlist whose marker cannot be read is held.
Ledger only.

---

## R-2061. A flagged routing tree whose only differences are untagged keeps its flag, and its refusal still says to run the rebuild

**Found:** at the review of #1061, R-2056, 2026-11-24.

**The mechanism.** A rebuild clears a tree's unconverged flag only when its after check converges, and an `untagged` vocal membership is a difference the additive rebuild cannot remove. `assert_converged`'s refusal (`tree-unconverged`) gives the step "run the rebuild for this tree", and `accept_as_it_stands` refuses a derivable tree. So a tree flagged by a restore whose remaining differences are untagged vocal memberships stays flagged until each is tagged or taken out, and the refusal does not say so.

**Measured cost.** Driven by the review on a disposable database: tagged, rebuilt, the association marked removed, the tree marked unconverged; the rebuild job exits 0 with the `vocal-membership-untagged` warning, the flag stays, and `route inbox` refuses with the rebuild step. The same holds before this branch for any `unexpected` leftover, the 484 on the live library among them, so R-2056 does not change whether the live tree clears today. The out of band restore detection that sets the flag was not driven.

**Closes when:** the unconverged refusal names, beside the rebuild, what a rebuild cannot settle (the leftovers and the untagged, taken out or tagged) when the last check found them. Ledger only: maintainer wording over a state that already existed.

---

## R-2062. The mirror edits, route inbox and the export bridge still file the vocal sub by the file's score, so a tagged track the account moves leaves its with vox and the resort puts it back

**Found:** at the review of #1061, R-2056, 2026-11-24.

**The mechanism.** R-2056 made the convergence check, `tree rebuild` and `route resort` file the vocal sub by the `vox` My Tag (U127), through `rebuild.derive_from_taxonomy`'s `carries_vox`. Three callers pass none and keep the score: `organize.mirror_edits._plan_genre`, which holds the database handle and the row's content id and REMOVES the held routed playlists its derivation does not want; `route inbox`'s plan, `routing_cli.plan_inbox`, which reads no database before its gate; and the export bridge, `routing_export._decide`. `mirror_edits.py` was left alone because #1058 (U958) was editing its removal path beside this card.

**Measured cost.** Driven by the review on the organize harness: a track tagged `vox` with no score, held in `Deep House / with vox`, moved on the account from Low to High; the mirror's change leaves `Deep House / with vox` and the track ends in High alone. After R-2056 the next `route resort` or `rebuild` adds it back, so the membership flips between verbs. In reverse, an untagged track over the cut that the account moves joins the new folder's `with vox` by the score, and `converge` then names it `untagged`. On the live library 2 tagged rows read under the cut and 607 untagged rows over it (R-2056), so the population is small but every one of them flips. `route inbox` files rows a landing has just tagged from the same score, so it disagrees only where the tag write failed or a person changed it; not measured.

**Closes when:** `mirror_edits._plan_genre` passes the tag's answer for its one row (`decision.content_id` in `write.vox_tag.vox_tagged(db) or frozenset()`, since the reader answers None for a library with no vox tag), with a test that a tagged track under the cut keeps or joins its `with vox` and an untagged one over the cut does not; and `route inbox` reads the tag for the rows it routes, or the GUIDE keeps saying it files by the score. Earns an issue under the board bar's (a): a verb removes a membership the product's own adoption wrote.

---

## R-2063. metadata mytags-vocals counts a vox association marked removed as already present, so it never tags that row again

**Found:** at the review of #1061, R-2056, 2026-11-24.

**The mechanism.** `rb_nodes.add_my_tag` asks `get_my_tag_songs(MyTagID, ContentID).first()` and reads no soft delete marker, so an association marked `rb_local_deleted` counts as present and `apply_mytags` reports the row `already`. `write.vox_tag.vox_tagged`, the reader every vocal filing path now asks, reads the marker and calls that row untagged (R-758). So a row whose file clears the cut and whose association is marked removed is named `untagged` by `converge` and is never tagged by the write that settles the rest.

**Measured cost.** Driven by the review on a disposable database: a row tagged, its association marked removed, then `apply_mytags` over it wrote 0, already 1, and the next rebuild still read `untagged`. R-2056's remedy text was reworded to send such a row to rekordbox. Whether rekordbox itself leaves a removed association as a soft delete is unmeasured (as R-843 says for the category), so whether a live row reaches this is not known.

**Closes when:** an attended read says whether rekordbox soft deletes a My Tag association it takes off; if it does, the writer reads the marker as the reader does. Ledger only: it closes at an attended sitting, and the product's text no longer claims the write settles it.

---

## R-2064. A frozen mirror plan answered after a bare sync pair paired the same WIP set copies it a second time

**Found:** at the review of #1062, U959, 2026-11-24.

**The mechanism.** `account_mirror._wip` reads the pair record at the plan
(`_paired`), and the run that answers the mirror's gate rebuilds from the
frozen library (R-1031, U222), reading no pair again. A bare `sync pair`
applied between the mirror's gate and its answer pairs a WIP set into `WIP `,
and the answer still creates the mirror's copy in `WIP`; the two titles
differ, so the plan's check for a person's playlist of the title does not
stop it.

**Measured cost.** Not driven end to end: the reviewer read the frozen
rebuild ignoring later rekordbox changes, which
`test_the_answering_run_applies_the_wip_plan_its_gate_showed` shows, and did
not run the interleave in one world. It needs a person to run a bare
`sync pair` between the two halves of a mirror run, which the sync pass never
does. Its reachability is unmeasured.

**Closes when:** the mirror's apply reads the pair record again and leaves a
WIP set a pair took since the gate, or the reverse rule makes the mirror's
copy the only one. Ledger only.

---

## R-2065. A sync pair answer stopped because the mirror copied a WIP set since the plan says the playlist was moved

**Found:** at the review of #1062, U959, 2026-11-24.

**The mechanism.** `sync/pair_check.py` discovers again before it writes,
now leaving out a WIP playlist the account mirror copies (U959). A set the
mirror copied between a bare `sync pair`'s plan and its answer is then no
longer found, and the check refuses `decision-stale` with "the rekordbox
playlist ... was moved since the plan, and is no longer one a sync of every
pair would make". Nothing moved: the mirror took it.

**Measured cost.** The stop and the replan are right and nothing is written,
driven by `test_a_wip_set_the_mirror_copies_after_the_plan_is_never_paired_at_the_answer`
with the ledger patched to the mirror's record; only the reason's words are
false. A real mirror apply between the two runs was not driven.

**Closes when:** the check names the mirror when the account mirror's ledger
holds the playlist's WIP title. Ledger only, a wording fix.

---

## R-2066. WIP playlists have two writers on the account, the mirror and a bare sync pair, and the choice between them is Phillip's

**Found:** at the review of #1062, U959, 2026-11-24.

**The mechanism.** A bare `crate sync pair` (U198) pairs every plain playlist
outside Cratekit's trees, WIP included, into an account root folder named as
the rekordbox top folder, `WIP ` with its trailing space; the 2026-11-05
sitting paired 9 WIP playlists that way, kept two ways. U959 adds the account
mirror's `WIP` folder, one way, its account edits held. Left alone the two
would copy one set twice. U959 takes the recommended option of the question
on the card: the mirror leaves a playlist a pair keeps, and a bare `sync pair`
leaves a WIP playlist the mirror already copies (`pair_discover.mirrored_wip`),
so each set has one copy, the 9 paired ones in `WIP ` and new ones in `WIP`.
The two other options were `sync pair` alone owning WIP, run by the sync pass,
or the mirror adopting the `WIP ` folder.

**Measured cost.** Two WIP folders on the phone, and a new set's edits on
Tidal are held, never taken back into rekordbox, where a paired set's are.
No copy is made twice, driven by `tests/test_sync_pair_discover_wip.py`.

**Closes when:** Phillip answers the card's question; option 1 needs nothing
more, options 2 and 3 are a card each. Ledger only.

---

## R-2067. A message catalogue made reachable after the suite configures is not read by argparse's stand in, which answers untranslated

**Found:** at the review of #985, U336, 2026-11-24.

**The mechanism.** `tests/conftest.py` asks `gettext.find` once, at `pytest_configure`, whether a catalogue exists for the default domain, and where none does it hands argparse `NullTranslations`' `gettext` and `ngettext` for the rest of the run. A catalogue that becomes reachable afterwards, by a test setting `LANGUAGE`, `LC_ALL`, `LC_MESSAGES` or `LANG`, or binding a domain, is read by `gettext.gettext` and not by the stand in: the review wrote a `messages.mo` mapping `usage: ` to `USO: `, bound it, set `LANGUAGE=xx` after configure, and `gettext.gettext` answered `USO: ` while argparse's stand in answered `usage: `.

**Measured cost.** None measured. Reachability is unmeasured: no test, source file, script or installed package sets a locale variable or calls `textdomain` or `bindtextdomain`, no `messages.mo` exists on the cloud container, and Phillip's Mac was not read. A test that did would read argparse's English where a person's machine would print the translation, which no test asserts today.

**Closes when:** a test that changes the locale or binds a domain runs with argparse on `gettext` itself (the conftest's `_give_argparse_its_lookups_back` and `_answer_argparse_untranslated` around it), or the conftest asks again where the environment changes. Ledger only.

---

## R-2068. The suite is 10 percent faster than at ff8e5ec on one container, not 30, since the rest of its time is product work and the mutation tables every whole tree read pays for

**Found:** at the build of #985, U336, 2026-11-24.

**The mechanism.** Point 5 of #847 (U290) asks the suite to run at least 30 percent faster than at `ff8e5ec`. Timed three times each, interleaved, on one four core container with nothing else running, `ff8e5ec` read 455.57, 444.50 and 447.93 seconds (median 447.93) and U336's branch at `6cfc857e` 410.04, 390.10 and 402.02 (median 402.02), a ratio of 0.898: 10.3 percent faster, where the bar is 313.55 seconds. A profile of the base `50022274` places the rest: the mutation tables under `docs/mutation` grew from 30 MB at `ff8e5ec` to 223 MB and every test reading every tracked file pays for them (the secret scan's reference proof, about 89 seconds, the repository scan in `tests/test_portability.py`, about 25); the crate parser is built 12,624 times a run, once per verb a test drives (about 86 core seconds after U336, 162 before); the collector takes 22 to 50 seconds a worker; and the workers wait on `fsync`, sqlite and subprocesses for about 15 percent of the cores' time. The suite also runs 2,000 more tests than at `ff8e5ec`. The test side levers that keep every guard are taken: U326's collector thresholds and walks, U312's parse sharing and walks, U336's argparse lookups and pin sweeps.

**Measured cost.** Maintainer facing: the epic's time bar is not met. No verb is affected.

**Closes when:** Phillip chooses one of the remaining levers, each a decision rather than a tuning, asked on #985: make a verb's subparser only when it is chosen (a change to `src/cratekit/cli`, about 25 seconds here), keep the battery's temporary files in memory or skip `fsync` (#702), keep the replay tables out of the tracked text the scans read, or rescope the bar. Ledger only.

---

## R-2069. On an uncalibrated library, an energy move taken from the account takes the track out of its folder's with vox, which the resort keeps and converge does not compare

**Found:** at the second review round of #1066, R-2062, 2026-11-24.

**The mechanism.** `organize/mirror_edits.py`, `_plan_genre`. With no vocal calibration the derivation places no vocal sub, so a held `with vox` of the moved track's own folder is not wanted, and being a routed playlist it is left. `_untagged_held` keeps an untagged vocal membership only where the tag is read, a calibrated library (R-2062), so nothing keeps it here. `tree rebuild` and `route resort` name the vocal dimension not compared and leave the membership, so the mirror is the one path that takes it out. The same on `main` before R-2062, the score placing nothing either.

**Measured cost.** Driven by the review on the organize harness: no calibration, a track tagged `vox` and held in `Deep House / with vox`, moved from Low to High on the account; the change leaves `Deep House / with vox`, and `converge` reports the tree converged before and after, the vocal sub not compared. Reachability unmeasured: no producer of a held `with vox` on an uncalibrated library was driven, since adoption and the resort file it only on a calibrated one; a library calibrated once and then uncalibrated would hold one.

**Closes when:** the mirror leaves a held vocal sub of the track's own folder alone wherever the vocal dimension is not compared, as the resort does, with a test on the uncalibrated harness. Ledger only: reachability is unmeasured and the behaviour is older than R-2062.

---

## R-2070. The CLI's portion narrowing in crate backup run is a second layer since U317, and kills no test

**Found:** at the replay of U290's survey kill set, U337, 2026-11-25.

**The mechanism.** u50-author W1 makes `if portion is not None:` in `src/cratekit/backup/cli.py` read `if False:`, so the CLI no longer narrows the plan to the named portion. Since U317 (`a94c7644`, a feature card outside U290) `plan_backup` plans only the named portion itself, so a backup asked for one portion still runs that portion alone, and the CLI's narrowing is a second layer covered by the first. Measured by the review on `tests/test_backup_cli.py`: at `a619edb0`, U317's parent, the mutant fails 14 tests against the unmutated control's 8, the six kills `docs/mutation/u337-replay/u337-survey-a.json` reads at the survey's commit; at `a94c7644`, 8 against 8. `u337-1.json` reads it zero on main.

**Measured cost.** None to a person: what a backup does is unchanged, and the refactor lost no kill here (`survey-before.json` names the row as changed by a feature card). A guard layer that kills nothing is maintainer facing (METHOD: remove each guard layer alone).

**Closes when:** the CLI's narrowing is removed as redundant with `plan_backup`'s, or a test drives the CLI with a plan that is not already narrowed and W1 is measured killed.

---

## R-2071. 38 guards the survey counted killed are killed by no Linux run, at the survey's commit or on main

**Found:** at the replay of U290's survey kill set, U337, 2026-11-25.

**The mechanism.** Each of these rows is recorded killed in its own unit's table, and so was counted in the 7,093 live killed rows of U290's survey, yet no test kills it on Linux: replayed on main (`docs/mutation/u337-replay/u337-1.json` to `u337-3.json`) and again at the survey's own commit `ff8e5ec` (`u337-survey-a`, `-b1`, `-b2a`, `-b2b`, `-r926.json`), every one read zero on the full suite, or died only of one of #702's inode tests, and at least one of its recorded killers runs on Linux (none is a known failure there). So the survey's own Linux tree did not kill them either: the kill its table recorded was taken on another machine, or on an earlier tree, or was a death of an unrelated test (several recorded killers are `tests/test_portability.py::test_the_repository_itself_is_clean` or the inode pair). The rows: `r1308.M10_count_unchecked` (modules/outbound/tidal_account.py), `r259.O1_no_tracks_guard` (label/sweep.py), `r259.O5_memo` (label/sweep.py), `r368-round-2.G6_ancestors_not_walked` (session/restore_cli.py), `r368-round-2.G14_the_destination_check_is_equality_only` (session/restore_cli.py), `r368.G5_paths_compared_as_strings` (session/restore_cli.py), `r424.B4_warning_copied` (favorites/cli.py), `r668-a.M11_no_frozen_list_skip` (acquire/cli.py), `r799-b.P6_one_file_is_one_group` (tagging/remap.py), `r923.N12_digest_drops_values` (write/row_defaults.py), `r926.G9_temporary_unresolved` (core/config.py), `u100-a.R1_slug_only_presence` (label/registry.py), `u112-b.A6_exported_not_product_made` (organize/account.py), `u113-a.A2_queue_order` (intake/account_playlists.py), `u116.M13_utc_year` (organize/filing.py), `u119.G16_read_back_blind_to_leftovers` (write/genre_favorites.py), `u125.D1_derive_test_tautology` (tests/test_reserved_causes.py), `u130-a.A1_removal_beats_addition` (sync/pair_merge.py), `u146-e.N3_owned_out_of_digest` (intake/native.py), `u165.F5_report_failed` (intake/filing.py), `u188.M5_repeat_kept` (intake/land_cli.py), `u190.G5_resume_one_job_only` (label/go.py), `u212.S2_download_refused_all` (cli/sync_land.py), `u212.S3_no_list_download` (cli/sync_land.py), `u214.M12_frozen_pairs` (organize/mirror_frozen.py), `u226.M18_waited_unformatted` (modules/outbound/tidal_account.py), `u227.R12_tree_filter` (organize/mirror_downloads.py), `u239.M07_beside_done` (label/go.py), `u28-skills-independent.S10_stamp_skill_name` (skills/cli.py), `u28-skills-independent.S13_expanduser` (skills/cli.py), `u28-skills-independent.S17_outcome_always_ok` (skills/cli.py), `u28-skills-independent.S20_packaged_root_via_file` (skills/cli.py), `u28-skills-independent.L9_command_comment_split` (tests/test_skills_lint.py), `u51-item-derivation.H1_export_item_not_payload` (export/cli.py), `u62.S7_naive_expiry_as_local` (acquire/provider_session.py), `u69-b.M16_next_command` (intake/missing_cli.py), `u71-b.B13_unlink_destination` (intake/landing.py), `u99-a.A13_by_name_unnormalized` (label/registry.py). Two more of the same kind, the gridless read back layer, have a residual of their own.

**Measured cost.** None of these is a kill U290 lost: each is named in `survey-before.json` as not killed at the survey on Linux. But each is a guard no test is shown to kill, and several sit on paths that write or delete (`session/restore_cli.py`, `write/row_defaults.py`, `write/genre_favorites.py`, `sync/pair_merge.py`, `intake/landing.py`, `intake/filing.py`, `organize/filing.py`), so the board bar (d) is met for those. Whether the macOS battery kills any of them is unmeasured.

**Closes when:** each row is measured on the macOS battery, and a row killed by no test anywhere gets a test that kills it, or is removed with the reason.

---

## R-2072. The read back layer of assert_created_rows_are_gridless kills no test, at the survey's commit or on main

**Found:** at the replay of U290's survey kill set, U337, 2026-11-25.

**The mechanism.** `assert_created_rows_are_gridless` in `src/cratekit/core/rb_writer.py` reads each row this session created back from SQL and refuses one carrying an analysis value. Two recorded guards of that read back are killed by no test: r746-a G7 (`if value not in EMPTY_ON_CREATE:` made `if False:`, so a value read from SQL is never a violation) and r746-d G5 (a content row held to the playlist tables' five columns, so a key or a rate rides in). Their recorded killers, `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit` and `::test_a_key_reaching_the_row_is_refused_from_sql_before_the_commit`, run and pass on Linux, and pass under either mutant: the taint they plant is refused by another layer first, so this layer, removed alone, is covered by nothing (METHOD: remove each guard layer alone).

**Measured cost.** Measured, not driven to a user: each mutant read zero on the full suite at `bd7fe681` (`docs/mutation/u337-replay/u337-1.json`) and at the survey's commit `ff8e5ec` (`u337-survey-a.json`); the one kill under U290, in U298's partial table, was all `tests/test_config_test_root.py`, the r926 folder. A guard on the guarded writer's path, the absolute rule against writing a beat grid, kills nothing (board bar d). Which layer refuses the taint first, and whether a planted value can reach SQL past it, is unmeasured.

**Closes when:** a test plants an analysis value that only the SQL read back can see (past the in memory judge and any later check) and both rows are measured killed, or the layer is shown redundant and removed with a composite naming what covers it.

---

## R-2073. The two inode tests of tests/test_repair_rows.py fail a full run at random on a cloud container, and read as kills

**Found:** at the replay of U290's survey kill set, U337, 2026-11-25.

**The mechanism.** `test_an_id_above_the_bound_that_is_the_files_inode_is_not_random` and `test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind` fail when run alone on these containers (both of them in three runs of three with the suite's options cleared here, one of them under the suite's own options) and fail inside a full parallel run some of the time, whatever the tree; #702 (U273) is where the battery learned they need a real disk. `cloud_battery.py baseline` records them as passing when its own full run passes them, so the driver does not subtract them, and a full run that fails one reads as a death of whatever row it measured.

**Measured cost.** On this card alone: three null controls killed by one of them (u337-librosa-1-0-0-b's first run, u337-survey-b2 and u337-survey-b2b's first run), each batch invalid and run again; seven rows read killed only by one of them in a promoted full run (u264 M7 under librosa 1.0.1; at ff8e5ec u130-a A1, r923 N12 and u28 L9 in survey a, u165 F5 in survey b1, r259 O1 and u112-b A6 in survey b2a), which `survey.py` now refuses or reads as no kill; and one subset baseline refused red (u115 F17 and F8, u272 S13, u193 M25, whose only killers they are, so those four rows are unmeasured on Linux). Helpers that added the two ids to a scratch copy of their known failures, as U334 recorded, avoided the first two costs; a hand added id is what the cloud unit skill forbids. Maintainer facing.

**Closes when:** the two tests are made deterministic on a container (or skipped where the filesystem cannot give the inode they need, named by the battery), so a full run reads them the same every time.

---

## R-2074. The single item export worker is never called by the job driver since U270

**Found:** at the build of #1073, R-2071, 2026-11-25.

**The mechanism.** `export.cli.handle` is the worker registered for `export.playlist`, and it carries `handle.batched = (handle_batch, BATCH)`. The job driver reads that attribute (`cli/handlers.py`, `BATCH_ATTRIBUTE`) and, once it names a valid batch form, hands every queued track to `handle_batch`, so `handle`'s own body, which exports one item through `run_export_item`, is reached by no drive. u51-item-derivation H1 mutated that body (the item's track taken from the payload instead of the item) and no test killed it; R-2071's card kills it with a test that calls `handle` directly on a queued job's item.

**Measured cost.** None to a user: the batch form is what runs. A maintainer reading `handle` sees a per item worker that production never calls, guarded by a test that drives it alone. Not driven past that: whether `handle` should be removed, leaving the batch form registered on its own, depends on whether the driver must keep a per item callable for a batch that fails whole, which was not measured.

**Closes when:** `handle` is shown needed by a path the driver takes and a test drives it through that path, or the registration names the batch form alone and `handle`'s body is removed with the test that drives it. Ledger only: maintainer facing.

---

## R-2075. Four layers beside the gridless read back kill no test, its pending source, its flush, its place inside the rollback, and the landing's after commit read back

**Found:** at the mutation table of #1074, R-2072, 2026-11-25.

**The mechanism.** `docs/mutation/r2072.md`, measured at `224eaf8d`, reads five rows at zero on the full suite, each confirmed by the driver's promotion. Of `assert_created_rows_are_gridless` in `src/cratekit/core/rb_writer.py`: S2, the read back takes only the binding's buffer and drops `session.new`; S3, the deliberate flush before the read back is skipped, so a still pending object has no identity and is passed over; S11, `commit_guarded` calls the read back after the block that rolls back on a refusal, so a refused session is left pending. Of `src/cratekit/intake/native.py`: L1, `assert_rows_gridless`, the read back after the commit, never refuses. And C11, S11's composite, the landing's own `trees.rollback_quietly` removed, also reads zero, alone and (review round two, on S11's subset) together with S11. The composites J1 and J2 (the whitelist's in memory judge disarmed) kill 22 each, but every kill is a literal `guard_violations` unit test, so they measure the judge and not what S2 and S3 protect.

**Measured cost.** Not driven to a user. S2 and S3: no producer was found; round one checked that the binding sets no default and no insert listener on any of the ten policy columns, and the rows a plain session add creates in production (my tags, lookup rows) carry no policy column, so a pending object's stored row is written by the guard's own flush from the values the whitelist has already judged. S11 and C11: no test catches the read back's refusal and commits again on the same handle, so "a refused write never lands later" is unmeasured for this refusal. L1: reached only when the guard before the commit has failed; under r2072 G7 it is what reports the committed row, but no test asserts its refusal. A guard on the writer's path that kills nothing is board bar (d).

**Closes when:** a test in `tests/test_rb_writer_db.py` plants a stored row violation on a disposable copy, catches the refusal from `commit_guarded`, commits again on the same handle and asserts nothing landed, killing S11; a test asserts `native.assert_rows_gridless`'s own refusal on a landed row, killing L1; and S2 and S3 are either killed by a pending creation carrying a stored value its object does not show, or named equivalent with that reasoning in a composite that is not a literal unit test.

---

## R-2076. U290's point 5 is short at its last measurement, test lines at 278,018 against 249,132 and the suite 11.4 percent faster than at ff8e5ec against 30, with 51 survey kills readable only on a Mac

**Found:** at the build of #987, U338, the last measurement of U290 (#847), 2026-11-25.

**The mechanism.** Point 5 of #847's definition of done: test lines at least 25 percent below the survey's 332,177, so at most 249,132; the full suite at least 30 percent faster on the cloud runner; every guard a test killed at the survey still killed. Measured on `main` at `147574d`:

- **Lines: 278,018** in 528 files by `scripts/refactor_measure.py table`, 28,886 over the bar, 16.3 percent below the survey. U315 read 289,090. By the numstat of the commits in `d289f61..147574d` over Python files, renames followed, grouped by the unit their subjects name (minus 11,096 in all, 24 more than the tree's 11,072, not traced further), the epic's further cards took 21,931 net off (U333 10,731, U335 5,903, U334 3,604, U332 2,557, against 864 added by U331, U336, U329 and U328), and feature cards outside the epic added 10,835 (U339 1,064, U340 973, R-1716 836, U958 825, U344 802 the largest). R-2048, R-2051 and R-2052 record why the four slices fell short of their shares.
- **Time: 11.4 percent faster, not 30.** `scripts/cloud_battery.py compare` three times a side on one four core container with nothing else running, `ff8e5ec` from its own clone and venv, interleaved: `main` 436.45, 422.78, 412.50 s, median **422.78**; `ff8e5ec` 476.91, 484.74, 432.59 s, median **476.91**; ratio 0.887 against the bar's 0.70 (333.84 s here). R-2068 records where the rest of the time goes.
- **Kill set: held on Linux, not whole.** U337's `survey.py join`, rebuilt at `147574d` against a clone of `ff8e5ec`, writes tables equal to the committed ones apart from their head and time, and `killset.py check` over them reads 6,883 owed, 5,302 killed as written, 1,576 at a new anchor, 5 mapped, **0 lost**; `check` over the 122 before and after pairs the records name exits 0 on 121, and the one exit 1, U332's batch 1 (u317 Q10), is its record's intermittent death, re-measured killed on both sides. Of the 210 rows left out, **51 cannot be read on Linux** (every killer fails here for the machine, or is one of the two inode tests R-2073 names), 40 were killed by no Linux run at the survey either (R-2071, R-2072; #1073, landed after `147574d` at `baafec32`, reads 37 of R-2071's 38 killed by new tests and one removed as an equivalent, and #1074 at `75c67934` R-2072's two killed by a new test), 82 had their text or guard changed by a feature card, and 37 were never killed under the epic.

**Measured cost.** Maintainer facing: the suite is larger and slower than the refactor was asked to leave it, and 51 survey kills are unproven until a Mac's test run reads them. No verb's behaviour is affected.

**Closes when:** the lines read at most 249,132 and the suite reads at most 0.70 of `ff8e5ec`'s time on one container, interleaved, and the 51 rows are read on a Mac, or Phillip retires the bars. By Phillip's decision of 2026-11-24 on #847, no further area card is filed for it, and by his rule of the same day no attended card for a mutation row. Ledger only.

---

## R-2077. U290's point 6 is short at its last measurement, the seventeen scripts at 7,444 lines against 7,374 and the three loaded documents at 1,001 against 975

**Found:** at the build of #987, U338, the last measurement of U290 (#847), 2026-11-25.

**The mechanism.** Point 6 of #847's definition of done, by U313's and U314's bars as U315 read them: the seventeen scripts the survey counted (`analyze_stages.py`, `board.py`, `calibrate_timing.py`, `ci_deps.py`, `cloud_battery.py`, `cloud_session.sh`, `cyanite_trial.py`, `dump_schemas.py`, `head_agreement.py`, `mutate.py`, `mutate_table.py`, `release.py`, `revendor_downloader.py`, `sample_name_shapes.py`, `scan_repo.py`, `title_differential.py`, `wait_ci.py`) at most 7,374 lines, `board.py` and `mutate.py` each under 1,500; the documents every build thread loads (`docs/METHOD.md`, `CLAUDE.md`, the cloud-unit skill) at most 975; the ledger in files of at most 5,000 lines, searchable. Measured by `wc -l` on `main` at `147574d`:

- the seventeen scripts **7,444**, 70 over. U330 left them at 7,360; U957 (`f9e0a663`, a feature card) added 116 to `scan_repo.py`, U343 took 33 off and U328 added 1. R-2036 recorded that crossing and closes on this measurement; this entry carries the shortfall from here.
- `board.py` 1,474 and `mutate.py` 1,191, both under 1,500, so that part holds. `scripts/refactor_measure.py`, outside the seventeen, is 1,591, over the 1,500 that U330's brief also read for every file in `scripts/`: U328 left it at 1,497 and U331 added 94.
- the three documents **1,001** (493, 141, 367), 26 over. U315 read 973 (487, 141, 345); the `merge(method)` of 2026-11-24 (`476696f9`, Phillip's rule that the macOS battery is owed by `main`) added 22 to the skill and 2 to METHOD, and U329, U336 and U331 together 4 to METHOD.
- the ledger: `docs/residual-findings.md` 1,006 lines and twelve archive files of at most 4,997, `board.py residuals --search` naming the archive file of each hit; this part holds.

**Measured cost.** Maintainer facing: every build thread loads 26 lines more than the bar, and the scripts stand 70 over theirs. No verb's behaviour is affected.

**Closes when:** the seventeen scripts read at most 7,374 lines, no file in `scripts/` is over 1,500 lines (`refactor_measure.py` included), and the three documents read at most 975, or Phillip retires the bars. By Phillip's decision of 2026-11-24 on #847, no further area card is filed for it. Ledger only.

---

## R-2078. U290's point 2 is short at its last measurement, src/cratekit at 195,379 lines against 193,000 and write/rebuild.py at 1,517 against 1,500

**Found:** at the build of #987, U338, the last measurement of U290 (#847), 2026-11-25.

**The mechanism.** Point 2 of #847's definition of done: `src/cratekit` outside `_vendor` at or under 193,000 lines, and no source file over 1,500. Measured by `scripts/refactor_measure.py table` and `lines --files` on `main` at `147574d`: **195,379 lines in 413 files**, 2,379 over the bar, and **one file over 1,500, `src/cratekit/write/rebuild.py` at 1,517**. U315 read 188,904 lines and `cli/registry.py` at 2,491 on `d289f61`; U328 took the registry under 1,500. Since `d289f61` the source grew by 6,475 lines. By the numstat of the commits in `d289f61..147574d` over Python files outside `_vendor`, renames followed, grouped by the unit their subjects name (6,479 in all, 4 more than the tree, not traced further), the epic's further cards added 156 net (U328 107, U331 84, U329 minus 35), and feature cards outside the epic 6,323, the largest U339 1,413, U958 1,229 and U340 1,109; `write/rebuild.py` crossed 1,500 by R-2056 and R-2062, a crossing R-2034 foresaw: no battery check holds the 1,500 line bar on a source file. R-2037 recorded the total passing 193,000 while the further cards built and closes on this measurement; this entry carries the shortfall from here.

**Measured cost.** Maintainer facing: the size the refactor was asked to reach is not where `main` stands. No verb's behaviour is affected.

**Closes when:** `refactor_measure.py table` reads at most 193,000 lines and 0 files over 1,500, or Phillip retires the bar. By Phillip's decision of 2026-11-24 on #847, no further area card is filed for it. Ledger only.

---

## R-2079. A failed writer rolls back the session and leaves the binding's update buffer and its playlist file, so a later commit on the handle bumps the update count and saves playlists that never landed

**Found:** at the review of #1077, R-2075, 2026-11-25.

**The mechanism.** `trees.rollback_quietly` in `src/cratekit/write/trees.py` calls `db.session.rollback()` and never the binding's own `db.rollback()`, which also clears pyrekordbox's process wide update buffer. After a failed native landing the buffer still holds the landing's creations and updates, and the binding's `commit` raises `agentRegistry.localUpdateCount` by one per buffered entry before it commits. Beside the buffer, the binding's `create_playlist` adds a node to its in memory `masterPlaylists6.xml`, which neither rollback removes, so the next commit saves nodes for playlists that have no row. Twenty one modules in `src/cratekit` unwind through `trees.rollback_quietly` (in `intake/`, `write/`, `tagging/`, `organize/`, `sync/`, `favorites/` and `analysis/`), and two private copies, `write/metadata_cli._rollback_quietly` and `sync/removed._rollback_quietly`, do the same.

**Measured cost.** Not driven to a user. The two reviews of #1077 drove the C11 test's shape on the disposable copy: after the landing failed, a later `db.commit()` on the same handle landed no row and no playlist row, but moved the update count from 100 to 137 (the binding's commit failing) and from 100 to 131 (the binding failing mid write); with `db.rollback()` in its place the buffer read 0 and the count did not move. With a minimal `masterPlaylists6.xml` planted beside the copy, the later commit wrote two nodes, the batch playlist and ANALYZE, under either rollback. No caller commits on a handle after a failed write: the two `native.apply_rows` callers (`intake/landing.py` and `intake/file_cli.py`) raise, seven other sites read raise too, and `open_db` clears the buffer for the next handle. Seven candidates were read and none commits after a failure.

**Closes when:** a failed write leaves neither the binding's buffer nor its playlist file holding what it rolled back (the binding's own `rollback` and the playlist file read again, or the handle closed), through the one helper and its two copies alike, and the C11 test in `tests/test_intake_land_native.py` also asserts the update count is unchanged after the later commit. Ledger only: no reachable producer.

---

## R-2080. An unreadable kept screen is dropped on load, so a gate it was the only sign of reads as nothing waiting

**Found:** at the review of #1080, U961, 2026-11-25.

**The mechanism.** `gates._screens_from` leaves out every entry
`Screen.from_json` refuses (not a mapping, a kind it does not know, a field
of the wrong type, `shown` that is not JSON), and the next save writes the
record without it. For most gates the run still says it waits, by its open
gate, an offer with no answer, or an answer bound to another plan, and `run
show` names the gate with `screen_missing`. One gate has no other sign: a gate
with no digest source refused for an option it does not offer leaves no
offer, no open gate and no answer, so with its screen unreadable
`gates.waiting` reads nothing waiting and `run show` carries `gate: null`.
Absence read as evidence of absence, METHOD's first pattern.

**Measured cost.** None observed. Reaching it needs a record whose screen was
damaged or written by a later shape; 0 candidates were driven to produce one,
so its reachability is unmeasured. Nothing is written by the run that reads
as clean; continuing it refuses at the gate again and keeps a fresh screen.

**Closes when:** an unreadable entry is kept as written and its gate named
with `screen_missing` saying the kept screen could not be read, with a test
over the unknown option case above. Ledger only.

---

## R-2081. Every reader that scans the run records parses each kept screen's plan, though only run show reads it

**Found:** at the review of #1080, U961, 2026-11-25.

**The mechanism.** `gates.RunState.from_json` turns every kept screen's
`shown`, JSON text of up to 64 KiB, into a mapping through `Screen.from_json`
on every load. The readers that scan every run record, `gates.siblings` on
each gated database verb and on `run decide`, `run retire`, the doctor's run
scan and `crate status`, load each record whole and never read a screen; only
`crate run show` does. U961 bounds which records hold one: `gates.record`
drops a gate's screen when it is answered or retired, and `Gates.require`
when it passes, so only a gate still waiting keeps one.

**Measured cost.** Driven at round one of the review: 300 records each
holding a cut screen of 70,026 bytes against the same 300 with none,
`gates.siblings` timed three times each, interleaved on one container: 0.118,
0.123 and 0.105 seconds against 0.013, 0.013 and 0.017, about 0.35 ms per kept
cut screen on every scan. How many unanswered gates with a large plan a real
state directory holds was not measured. Slowness only: nothing is lost or
misread.

**Closes when:** a screen's `shown` is parsed only when `run show` asks for
it, with a timing test holding a scan of records with cut screens to the
ratio of one without, or the count of kept screens in a real state directory
is read at an attended sitting and found small. Ledger only.

---

## R-2082. Doctor's backup age checks read an ejected library volume as never recorded

**Found:** at review round two of #1079, U960, 2026-11-25.

**The mechanism.** The backup facts file is library scoped (`state_files`
`_library("backup_facts")`), and `backup_facts._read` takes a missing file
for no fact. `doctor_backup._check_backup_portion` calls `backup_facts.ages`
with no mount gate, while `_check_backup_acknowledgment` beside it asks
`_library_state_unreadable` first. So with the library root absent, as
`/Volumes/<name>` is after an eject, `backup.age.files` and
`backup.age.database` read INFO "no completion has been recorded for this
portion here, which is the state of every library before a backup has run
once". U960's glance asks `core.preflight`'s rule first and reads the same
state unreadable, so doctor and the glance now disagree on that input.

**Measured cost.** Driven on the branch at `f10a9afb`: the root renamed
away, `crate --output json doctor` read both portions as never recorded. A
person is told no backup exists when the record is on the unplugged drive;
doctor reports the volume in its own rows, but these two rows say something
false (board bar b). On main before U960, unchanged by it.

**Closes when:** `_check_backup_portion` asks `_library_state_unreadable`
before reading and answers its note, as the acknowledgment check does, with
a test that renames the root and reads both rows. It earns an issue under
the board bar's (b), a clean report over state it could not read.

---

## R-2083. The status glance reads a running job whose driver died as running until something reconciles it

**Found:** at review round one of #1079, U960, 2026-11-25.

**The mechanism.** The glance lists jobs in state `running` off the queue,
as `crate job list --state running` does. A job whose driver was killed
keeps `running` in the queue until `crate job show` or a resume reconciles
it against its driver lock (`jobs.reconcile`), which a read only glance does
not do.

**Measured cost.** Driven with a job moved to `running` and no driver lock
held: the glance and `job list` both read `running`, and `attention` reads
`running`; after `crate job show` reconciled it to `queued`, the glance read
`ok`. A killed driver, the real producer, was not driven. The menu bar icon
would say running for work nothing is doing.

**Closes when:** the menu bar app's card (#1085) decides whether the glance
asks the driver lock read only (`jobs.assert_free` without the reconcile) so
a job with no live driver reads apart from one that runs. Ledger only.

---

## R-2084. crate status reads every run record twice, and each call of it adds one

**Found:** at review round one of #1079, U960, 2026-11-25.

**The mechanism.** `crate status` lists and loads every run record for its
own run lines (`doctor._run_report`) and again for the glance
(`status_glance.gate_runs`), and the dispatcher saves a run record for every
verb, `status` included, so an app that polls the verb grows the directory
it reads by one record a call.

**Measured cost.** At 20,000 records, three repeats on the cloud container:
the glance's scan 0.65 to 0.88 seconds, `_run_report` 0.66 to 0.73, the
whole verb 1.39 to 1.54. At 200 records the verb answered in 0.40 to 0.69.
An app polling once a minute adds 1,440 records a day; the count on
Phillip's machine is unmeasured.

**Closes when:** the status verb loads the records once and hands them to
both readers, and the menu bar app's card decides whether its polling verb
records a run at all. Ledger only.

---

## R-2085. A night pass waiting at the acknowledgment leaves the status glance's attention at ok

**Found:** at review round one of #1079, U960, 2026-11-25.

**The mechanism.** `attention` reads `gate` from the run records with an
open gate. A night pass that stopped at `waiting-at-acknowledgment`, or at
plain `waiting`, holds no open gate, so `attention` can read `ok` while
`night.outcome` says the pass waits on a person. The brief's precedence
names no night word, and the glance carries the outcome for the app.

**Measured cost.** Read, not driven: the producer, a night pass stopping at
the acknowledgment, was not driven. The icon would read `ok` while a pass
waits; the glance's `night` key says so to anything that reads it.

**Closes when:** the menu bar app's card (#1085) decides whether a waiting
night outcome raises the icon, and if so the glance's `attention` takes it.
Ledger only.

---

## R-2086. Runs waiting on a pending action with no open gate are not in the status glance

**Found:** at the plan of #1079, U960, 2026-11-25.

**The mechanism.** The glance's `gates` lists runs with an open gate, each
with the gate's options, as the brief's shape asks. A run that waits on a
pending human action and no gate has nothing to answer through
`crate run decide`, so it is left out; `crate status`'s own check lines still
list it as awaiting that action.

**Measured cost.** Driven only as a run saved with no gate, which reads
`gates` empty; a run carrying a pending action was read, not driven. An app
reading the glance alone does not see such a run.

**Closes when:** the menu bar app's card decides whether a pending action is
shown, and the glance gains a key for it with a schema version bump. Ledger
only.

---

## R-2087. An unplugged library drive reads the status glance's attention as fail for as long as it is unplugged

**Found:** at review round two of #1079, U960, 2026-11-25.

**The mechanism.** The backup record is on the library volume, so with the
drive unplugged the glance reads `backup` unreadable and `attention` `fail`,
as the brief's rule for an unreadable source asks; the human line reads
`attention: fail (backup unreadable)`.

**Measured cost.** Driven with the root renamed away. On a laptop that is
often away from its library drive, the icon would read `fail` for the
ordinary state of being unplugged.

**Closes when:** the menu bar app's card (#1085) decides whether an absent
volume earns a word of its own ahead of `fail`. Ledger only.

---

## R-2088. a job a chain drives in under a second never reports running under --progress json

**Found:** at the review of #1082, U963, 2026-11-25.

**The mechanism.** Under `--progress json` the job watch in
`src/cratekit/cli/progress.py` reads the job off the queue once as the drive
starts, then every `WATCH_SECONDS` (one second) and once after the drive. A
job whose whole drive is shorter than the interval goes from `queued` to its
settled state between two readings, so the stream says `queued` then
`succeeded` and never `running`. The brief asks for at least one event per
state change while a chain waits on a job.

**Measured cost.** Driven by the review at the shipped interval, two items of
0.2 seconds each: `queued`, then `succeeded`. No one is told anything false:
the job's last event is its settled state as the queue holds it, and a job
long enough for an app to show it running (a download, an analysis of a real
pass) is read while it runs. A shorter interval reads the queue more often
for every driven job.

**Closes when:** the engine announces each transition it makes, rather than
the watch sampling it, or the sampling is judged enough. Ledger only:
maintainer facing, nothing is lost or misreported.

---

## R-2089. crate sync night under --progress json writes only its end, none of its nested pass's steps or jobs

**Found:** at the review of #1082, U963, 2026-11-25.

**The mechanism.** `sync night` runs its nested `sync land` through
`tail.dispatch`, which calls the dispatcher with `--output json` and no
`--progress`, and keeps the child's standard error in memory. So under
`crate --output json --progress json sync night` the pass's fifteen or so
child commands write no event, and the stream is one `end`. Human output of
`sync night` shows none of the pass's steps either, so the flag matches it.

**Measured cost.** Driven by the review in process over the suite's fakes:
fifteen child commands ran and the only event was `end`. No producer asks
for it: the scheduled night's command, `schedule.py`'s `NIGHT_ARGV`, passes
no flag, and the menu bar app's Sync (U967) runs `sync land`, which streams.
The guide says to follow a pass with `sync land`.

**Closes when:** a card has the app follow a night pass, which hands the
night's writer to its nested pass as `run decide --continue` does, or the
night is judged to need no stream. Ledger only: nothing is misreported, and
no workflow is blocked.

---

## R-2090. The app's runner shows a verb that printed a whole envelope and then died of a signal as a signal death alone

**Found:** at the review round two of #1084, U965, 2026-11-25.

**The mechanism.** `CrateRunner.runBlocking` returns `.signalled` whenever `terminationReason` is an uncaught signal, before it reads standard output, so a verb that printed a complete envelope and then died of a signal (in interpreter shutdown, say) is shown only as a signal death, its envelope dropped. The fix round chose this so a signal's number is never read as one of crate's exit codes (a SIGBUS, 10, read as a gate).

**Measured cost.** Argued from reading only; no verb was driven to die of a signal after printing its envelope, and no shipped caller runs a verb yet.

**Closes when:** the card that first shows a verb's result in the app carries the envelope, when one decodes, beside the signal in the `.signalled` case, with a test over a fake that prints an envelope and then kills itself. Ledger only.

---

## R-2091. The app's runner signals a timed out verb's own process and not its children, reports a verb a SIGKILL has not yet ended as ended, and gives a job three seconds to stop cleanly

**Found:** at the reviews of #1084, U965, 2026-11-25.

**The mechanism.** `CrateRunner.runBlocking` in `app/Sources/CrateEngine/CrateRunner.swift` sends SIGTERM to crate's own pid at the timeout, then SIGKILL after `terminationGrace`, three seconds, and signals no other process. A child crate started (rclone, ffmpeg, a pool worker) is not signalled and keeps running after the app reports `timedOut`. swift-corelibs-foundation starts the child in a process group of its own (`POSIX_SPAWN_SETPGROUP`, its commit faef552, which says this matches Darwin), so signalling the group, `kill(-pid, ...)`, may be enough; whether Apple's Foundation does the same was not driven. After the SIGKILL the wait is bounded by the same grace, so a verb a SIGKILL has not ended within it (one held in uninterruptible I/O on a hung volume) is reported as `timedOut`, whose comment says ended. A job driver that stops cleanly on SIGTERM at an item boundary may need longer than three seconds, and every call defaults to a 60 second timeout whatever the verb.

**Measured cost.** On Linux the review killed only a fake shell's pid and its `sleep` child stayed in the group, holding the pipe 0.71 seconds; on the App workflow `testAVerbThatIgnoresTerminateIsKilled` takes about 4.2 seconds, 0.9 past its timeout and grace, the orphaned `sleep 1` holding the pipe. The unkillable case was not driven: no test environment holds a process SIGKILL cannot end. No shipped caller runs a long verb, since the app in U965 only shows the crate setup state, so nobody pays today; the cost lands when a later card runs `sync` or a job through the runner.

**Closes when:** the card that first runs a long verb through the runner (the Sync card) ends the whole group, reports a verb still running after the kill as still running, sets a timeout per verb, and gives a job driver the grace it needs to stop at an item boundary, each with a test over a fake that leaves a child. Ledger only: no shipped caller pays it.

---

## R-2092. No app fixture carries a pending human action, so a change to that shape passes the fixture guard

**Found:** at the review of #1084, U965, 2026-11-25.

**The mechanism.** `tests/test_app_fixtures.py` holds three envelopes to the real verbs (doctor, a gate refusal, a refusal with steps). None has a `pending_human_action`, and the Swift test of that shape decodes a dictionary built by hand. The review renamed `verify_verb` in `PendingHumanAction.to_json` and all six fixture tests passed.

**Measured cost.** Driven by the review on 13e3eee: the rename passes the battery. No shipped caller reads a pending action yet, so nobody pays today; a pending envelope from `sync land` would decode as undecodable in the app once a card reads one.

**Closes when:** the first card that reads a pending action in the app (the Sync card) adds a fixture from a real verb that leaves one, and its Swift test decodes that fixture. Ledger only.

---

## R-2093. crate started by the app inherits the app's controlling terminal when the app was started from one, so the session reads a person at a terminal

**Found:** at the review of #1084, U965, 2026-11-25.

**The mechanism.** `CrateRunner` sets standard input to the null device but cannot detach crate from the app's session, since Foundation's `Process` has no `setsid`. When the app is started from Terminal (as `swift run` does), crate's `has_controlling_terminal` in `cratekit.core.session` finds the terminal, so a gate answered through the app may be recorded as answered at the command line. The app started from Finder or as a login item has no terminal and is unaffected.

**Measured cost.** Argued from reading; not driven, since no container runs Swift and the app in U965 runs no gated verb.

**Closes when:** the gate card (the one gate view) starts crate in a new session, or passes the actor explicitly, and a test reads the recorded actor of a gate answered through the runner. Ledger only.

---

## R-2094. The app decodes every JSON number in a verb's data as a Double, so an integer above two to the fifty third loses precision

**Found:** at the review of #1084, U965, 2026-11-25.

**The mechanism.** `JSONValue` in `app/Sources/CrateEngine/JSONValue.swift` holds every number as `Double`. An integer above 2^53 in a verb's `data` or a cause's `detail`, such as a 64 bit database id, would read back rounded.

**Measured cost.** Not driven. The review found no verb that emits an integer above 2^53 into an envelope; the envelope's own integers (`envelope`, `exit_code`, `code`) are decoded as `Int`. No shipped caller reads such a field.

**Closes when:** a card that shows a large integer from a verb's data keeps integers whole (an integer case in `JSONValue`, decoded before the double), with a fixture carrying one. Ledger only.

---

## R-2095. Other readers of library scoped state read an absent volume as no state, unmeasured

**Found:** at review round one of #1093, R-2082, 2026-11-25.

**The mechanism.** The class of R-2082 one file over, named by the review
and not driven: `backup_facts.ages` is also read with no mount gate by
`backup/cli.py` and `modules/tools/backup.py`, and doctor reads two more
library scoped files the same way, the vocal calibration
(`doctor_model._vocals_scored`) and the taxonomy origin
(`doctor_library.py`). Off an ejected volume each would take a missing file
for none.

**Measured cost.** Not driven, so unmeasured: whether any of them says
something false to a person, or refuses first on the volume through a gate
of its own, was not established. The backup verb is known to refuse
`library-root-unproven` before it reads anything of the library.

**Closes when:** each is driven with the root renamed away and either gated
by `core.preflight.library_state_is_readable` with a test, or shown to
refuse on the volume first. Ledger only, until one is driven to a false
sentence.

---

## R-2096. The backup acknowledgment reads an ejected library volume's backup ages as never recorded, and the terminal rule mints over them

**Found:** at review round one of #1093, R-2082, 2026-11-25.

**The mechanism.** `session_ack._shown_ages` calls `backup_facts.ages` with
no mount gate, and the backup record is library scoped, so off an ejected
volume the missing file reads as no fact. The session rule then refuses with
`backup-acknowledgment-backup-too-old`, saying the files portion's age is not
known (never-recorded) and to run a backup first. The terminal rule mints
over the same never recorded ages and writes the acknowledgment under the
configured root, recreating the root's state folder where the volume should
mount. Doctor's backup rows ask `core.preflight`'s rule first since R-2082;
this reader does not.

**Measured cost.** Driven at `46830cb7`: both portions recorded a day ago,
the library root renamed away. `crate --output json session ack --as
session` exits 32 with the false advice; nothing is lost, since it refuses.
`session_ack.record_acknowledgment(cfg, terminal=lambda: True)` minted over
never recorded ages and recreated the root's state folder, driven through the
terminal seam, not through the gate a person answers. On a Mac that folder
would sit at the volume's mount point on the boot disk (board bar b, and d
for the write).

**Closes when:** `_shown_ages`, or `record_acknowledgment` before it, asks
`core.preflight.library_state_is_readable` for the mount and refuses with a
cause naming the absent volume, never reading the ages or writing; tests
rename the root and drive both rules through the CLI. Earns an issue under
the board bar's (b), the product saying something false, and (d), a write
with no guard against an absent volume.
